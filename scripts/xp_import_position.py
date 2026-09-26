#!/usr/bin/env python3
"""Import the Tesouro Direto section of one XP PosicaoDetalhada workbook."""

import argparse
import csv
import posixpath
import re
import tempfile
import unicodedata
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "inbox" / "XP"
OUTPUT = ROOT / "state" / "positions" / "tesouro_direto.csv"
PENDING = "[pending]"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
CSV_FIELDS = (
    "ticker", "description", "type", "investment_date", "due_date",
    "quantity", "available", "acquisition_price",
)
EXPECTED_HEADERS = {
    "B": "Saldo", "C": "% Alocação", "D": "Valor aplicado",
    "E": "Quantidade", "F": "Disponível", "G": "Vencimento",
}


def read_sheet(archive):
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    sheets = workbook.findall(f"{NS}sheets/{NS}sheet")
    chosen = [sheet for sheet in sheets if sheet.get("name") == "Sua carteira"]
    if len(chosen) != 1:
        raise ValueError("A aba 'Sua carteira' não foi encontrada exatamente uma vez")
    relationship_id = chosen[0].get(f"{REL_NS}id")
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    relation = next((node for node in relationships if node.get("Id") == relationship_id), None)
    if relation is None or not relation.get("Target"):
        raise ValueError("Não foi possível localizar a aba 'Sua carteira' no XLSX")
    target = relation.get("Target")
    sheet_path = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
    if not sheet_path.startswith("xl/worksheets/"):
        raise ValueError("Caminho da aba inesperado no XLSX")
    shared = []
    if "xl/sharedStrings.xml" in archive.namelist():
        strings = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        shared = ["".join(node.text or "" for node in item.iter(f"{NS}t")) for item in strings.findall(f"{NS}si")]
    sheet = ET.fromstring(archive.read(sheet_path))
    rows = []
    for row in sheet.findall(f"{NS}sheetData/{NS}row"):
        values = {}
        for cell in row.findall(f"{NS}c"):
            column = re.match(r"[A-Z]+", cell.get("r", ""))
            if column is None:
                continue
            value = cell.find(f"{NS}v")
            inline = cell.find(f"{NS}is")
            content = (value.text or "") if value is not None else ""
            if cell.get("t") == "s" and content:
                content = shared[int(content)]
            elif cell.get("t") == "inlineStr" and inline is not None:
                content = "".join(node.text or "" for node in inline.iter(f"{NS}t"))
            values[column.group()] = content.strip()
        rows.append((int(row.get("r")), values))
    return rows


def decimal_br(value, row_number, field):
    normalized = value.strip().replace("R$", "").replace(" ", "")
    if "," in normalized:
        if not re.fullmatch(r"(?:\d{1,3}(?:\.\d{3})+|\d+),\d+", normalized):
            raise ValueError(f"Linha {row_number}: {field} inválido: {value!r}")
        normalized = normalized.replace(".", "").replace(",", ".")
    elif not re.fullmatch(r"\d+(?:\.\d+)?", normalized):
        raise ValueError(f"Linha {row_number}: {field} inválido: {value!r}")
    try:
        number = Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError(f"Linha {row_number}: {field} inválido: {value!r}") from exc
    if not number.is_finite() or number < 0:
        raise ValueError(f"Linha {row_number}: {field} deve ser não negativo")
    return number


def iso_date(value, row_number, field="vencimento"):
    try:
        return datetime.strptime(value, "%d/%m/%Y").date().isoformat()
    except ValueError as exc:
        raise ValueError(f"Linha {row_number}: {field} inválido: {value!r}") from exc


def bond_type(description):
    folded = unicodedata.normalize("NFKD", description).encode("ascii", "ignore").decode("ascii").upper()
    if re.match(r"^(LFT|TESOURO SELIC)(?:\s|$)", folded):
        return "pos"
    if re.match(r"^(LTN|NTN-F|TESOURO PREFIXADO)(?:\s|$)", folded):
        return "pre"
    if re.match(r"^(NTN-B1?|TESOURO IPCA|TESOURO RENDA\+|TESOURO EDUCA\+)(?:\s|$)", folded):
        return "ipca"
    return PENDING


def assign_sequential_tickers(records):
    original_tickers = {record["ticker"] for record in records}
    used_tickers = set()
    next_sequence = {}
    for record in records:
        base = record["ticker"]
        if base not in used_tickers:
            used_tickers.add(base)
            next_sequence[base] = 2
            continue
        sequence = next_sequence[base]
        while f"{base}_{sequence}" in original_tickers or f"{base}_{sequence}" in used_tickers:
            sequence += 1
        record["ticker"] = f"{base}_{sequence}"
        used_tickers.add(record["ticker"])
        next_sequence[base] = sequence + 1
    return records


def import_rows(rows):
    markers = [(index, number, cells) for index, (number, cells) in enumerate(rows) if cells.get("A", "").casefold() == "tesouro direto"]
    if len(markers) != 1:
        raise ValueError("A seção 'Tesouro Direto' não foi encontrada exatamente uma vez")
    start, section_line, marker = markers[0]
    expected_balance = decimal_br(marker.get("G", ""), section_line, "total Tesouro Direto")
    header_seen = False
    balance_total = Decimal(0)
    records = []
    for number, cells in rows[start + 1:]:
        populated = {column: cells.get(column, "") for column in "ABCDEFG"}
        if not any(populated.values()):
            continue
        if populated["A"] and not any(populated[col] for col in "BCDEF") and populated["G"].startswith("R$"):
            break
        if all(populated[col] == label for col, label in EXPECTED_HEADERS.items()):
            header_seen = True
            continue
        if not header_seen:
            raise ValueError(f"Linha {number}: layout inesperado antes do cabeçalho Tesouro Direto")
        description = populated["A"]
        if not description:
            raise ValueError(f"Linha {number}: título Tesouro sem descrição")
        ticker = description.replace(" ", "_")
        balance_total += decimal_br(populated["B"], number, "saldo")
        if populated["D"]:
            decimal_br(populated["D"], number, "valor aplicado")
        quantity = decimal_br(populated["E"], number, "quantidade") if populated["E"] else None
        available = decimal_br(populated["F"], number, "disponível") if populated["F"] else None
        if quantity is not None and available is not None and available > quantity:
            raise ValueError(f"Linha {number}: quantidade/disponível incompatíveis")
        record = {
            "ticker": ticker,
            "description": description,
            "type": bond_type(description),
            "investment_date": PENDING,
            "due_date": iso_date(populated["G"], number) if populated["G"] else PENDING,
            "quantity": str(quantity) if quantity is not None else PENDING,
            "available": str(available) if available is not None else PENDING,
            "acquisition_price": PENDING,
        }
        records.append(record)
    if not header_seen or not records:
        raise ValueError("Seção Tesouro Direto sem cabeçalho ou títulos")
    if balance_total != expected_balance:
        raise ValueError(f"Total Tesouro Direto divergente: linhas={balance_total}, seção={expected_balance}")
    return assign_sequential_tickers(records)


def _read_existing(output, fieldnames, legacy_defaults):
    output = output or OUTPUT
    if not output.exists():
        return [], False
    with output.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        migrated = bool(legacy_defaults) and reader.fieldnames == [field for field in fieldnames if field not in legacy_defaults]
        if reader.fieldnames != list(fieldnames) and not migrated:
            raise ValueError(f"Cabeçalho incompatível em {output}")
        records = list(reader)
    if migrated:
        for record in records:
            record.update(legacy_defaults)
    seen = set()
    for record in records:
        ticker = record["ticker"]
        if not ticker or ticker in seen or None in record or any(value is None for value in record.values()):
            raise ValueError(f"ID ausente/duplicado ou linha inválida em {output}")
        seen.add(ticker)
    return records, migrated


def read_existing(output=None, fieldnames=CSV_FIELDS):
    records, _ = _read_existing(output, fieldnames, None)
    return records


def write_csv(records, output=None, fieldnames=CSV_FIELDS, legacy_defaults=None):
    output = output or OUTPUT
    existing, migrated = _read_existing(output, fieldnames, legacy_defaults)
    known = {record["ticker"] for record in existing}
    additions = [record for record in records if record["ticker"] not in known]
    if not additions and not migrated:
        return 0, len(existing)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=output.parent, prefix=f".{output.stem}-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing + additions)
        temporary.replace(output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return len(additions), len(existing)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename", help="Nome do XLSX dentro de inbox/XP")
    args = parser.parse_args()
    if Path(args.filename).name != args.filename or not args.filename.lower().endswith(".xlsx"):
        parser.error("informe apenas o nome de um arquivo .xlsx de inbox/XP")
    source = INBOX / args.filename
    if not source.is_file() or not source.resolve().is_relative_to(INBOX.resolve()):
        parser.error(f"arquivo não encontrado em inbox/XP: {args.filename}")
    with ZipFile(source) as archive:
        records = import_rows(read_sheet(archive))
    added, preserved = write_csv(records)
    print(f"{added} título(s) novo(s); {preserved} registro(s) existente(s) preservado(s) em {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, IndexError, OSError, BadZipFile, ET.ParseError) as exc:
        raise SystemExit(f"Erro: {exc}") from exc
