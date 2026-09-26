#!/usr/bin/env python3
"""Import the Previdência Privada section of one XP PosicaoDetalhada workbook."""

import argparse
import re
import unicodedata
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

if __package__:
    from .xp_import_position import INBOX, PENDING, ROOT, assign_sequential_tickers, decimal_br, read_sheet, write_csv
else:
    from xp_import_position import INBOX, PENDING, ROOT, assign_sequential_tickers, decimal_br, read_sheet, write_csv

OUTPUT = ROOT / "state" / "positions" / "previdencia_privada.csv"
SECTION = "Previdência Privada"
HEADERS = {"D": "Saldo", "E": "% Alocação", "F": "Rendimento bruto", "G": "Valor aplicado"}


def pension_type(category):
    folded = unicodedata.normalize("NFKD", category).encode("ascii", "ignore").decode("ascii").casefold()
    if folded == "pos-fixado":
        return "pos"
    if folded == "prefixado":
        return "pre"
    if folded == "inflacao":
        return "ipca"
    if folded == "multimercados":
        return "multi"
    return PENDING


def import_rows(rows):
    markers = [(index, number, cells) for index, (number, cells) in enumerate(rows) if cells.get("A", "").casefold() == SECTION.casefold()]
    if len(markers) != 1:
        raise ValueError(f"A seção {SECTION!r} não foi encontrada exatamente uma vez")
    start, section_line, marker = markers[0]
    expected_balance = decimal_br(marker.get("G", ""), section_line, "total Previdência Privada")
    records = []
    category = None
    balance_total = Decimal(0)
    for number, cells in rows[start + 1:]:
        populated = {column: cells.get(column, "") for column in "ABCDEFG"}
        if not any(populated.values()):
            continue
        if populated["A"] and not any(populated[col] for col in "BCDEF") and populated["G"].startswith("R$"):
            break
        if all(populated[col] == label for col, label in HEADERS.items()):
            if not re.search(r"\|\s*\S", populated["A"]):
                raise ValueError(f"Linha {number}: categoria de Previdência Privada ausente")
            category = pension_type(populated["A"].split("|", 1)[1].strip())
            continue
        if category is None:
            raise ValueError(f"Linha {number}: layout inesperado antes do cabeçalho Previdência Privada")
        description = populated["A"]
        if not description:
            raise ValueError(f"Linha {number}: fundo de previdência sem descrição")
        ticker = description.replace(" ", "_")
        balance_total += decimal_br(populated["D"], number, "saldo")
        applied = decimal_br(populated["G"], number, "valor aplicado") if populated["G"] else None
        records.append({
            "ticker": ticker,
            "description": description,
            "type": category,
            "investment_date": PENDING,
            "due_date": "",
            "quantity": "1",
            "available": "1",
            "acquisition_price": str(applied) if applied is not None else PENDING,
        })
    if not records:
        raise ValueError("Seção Previdência Privada sem cabeçalho ou fundos")
    if balance_total != expected_balance:
        raise ValueError(f"Total Previdência Privada divergente: linhas={balance_total}, seção={expected_balance}")
    return assign_sequential_tickers(records)


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
    added, preserved = write_csv(records, OUTPUT)
    print(f"{added} fundo(s) novo(s); {preserved} registro(s) existente(s) preservado(s) em {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, IndexError, OSError, BadZipFile, ET.ParseError) as exc:
        raise SystemExit(f"Erro: {exc}") from exc
