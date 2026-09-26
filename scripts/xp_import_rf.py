#!/usr/bin/env python3
"""Import the Renda Fixa section of one XP PosicaoDetalhada workbook."""

import argparse
import re
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

if __package__:
    from .xp_import_fii import integer_br
    from .xp_import_position import CSV_FIELDS, INBOX, PENDING, ROOT, assign_sequential_tickers, decimal_br, iso_date, read_sheet, write_csv
else:
    from xp_import_fii import integer_br
    from xp_import_position import CSV_FIELDS, INBOX, PENDING, ROOT, assign_sequential_tickers, decimal_br, iso_date, read_sheet, write_csv

OUTPUT = ROOT / "state" / "positions" / "renda_fixa.csv"
SECTION = "Renda Fixa"
CSV_FIELDS_RF = (*CSV_FIELDS, "market_rentability", "isin", "issuer", "investment_type")
ISSUER_DESCRIPTION = re.compile(
    r"^(CDB|CRA|CRI|DEB|LCA|LCD|LF|FND) (.+) - "
    r"(?:JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)/\d{4}$"
)
HEADERS = {
    "B": "Saldo a mercado", "C": "% Alocação", "D": "Valor aplicado",
    "E": "Valor aplicado original", "F": "Rentabilidade a mercado",
    "G": "Data aplicação", "H": "Data vencimento", "I": "Quantidade",
    "J": "Preço Unitário", "K": "IR", "L": "IOF", "M": "Saldo líquido",
}


def parse_issuer(description):
    match = ISSUER_DESCRIPTION.fullmatch(description)
    if not match:
        return PENDING
    issuer = match.group(2).removesuffix(" - JURO MENSAL").strip()
    return issuer or PENDING


def parse_investment_type(description):
    """Extract investment type from description (CDB, LCA, LCD, LF, CRA, CRI, DEB, FND)."""
    match = ISSUER_DESCRIPTION.fullmatch(description)
    if match:
        return match.group(1)
    return PENDING


def classify_rentability_type(rentability):
    """Classify rentability into pre, pos, or ipca based on the text."""
    if not rentability or rentability == PENDING:
        return PENDING

    rentability_upper = rentability.upper()

    # IPCA or IPC-A (inflation indexed)
    if "IPCA" in rentability_upper or "IPC-A" in rentability_upper:
        return "ipca"

    # CDI (post-fixed)
    if "CDI" in rentability_upper:
        return "pos"

    # Pre-fixed: starts with + without CDI, or contains % with a.a./a.m. without CDI/IPCA
    if (rentability.strip().startswith("+") and "CDI" not in rentability_upper) or \
       ("%" in rentability and ("A.A." in rentability_upper or "A.M." in rentability_upper) and \
        "CDI" not in rentability_upper and "IPCA" not in rentability_upper and "IPC-A" not in rentability_upper):
        return "pre"

    return PENDING


def import_rows(rows):
    markers = [(index, number, cells) for index, (number, cells) in enumerate(rows) if cells.get("A", "").casefold() == SECTION.casefold()]
    if len(markers) != 1:
        raise ValueError(f"A seção {SECTION!r} não foi encontrada exatamente uma vez")
    start, section_line, marker = markers[0]
    expected_balance = decimal_br(marker.get("G", ""), section_line, "total Renda Fixa")
    header_seen = False
    balance_total = Decimal(0)
    records = []
    for number, cells in rows[start + 1:]:
        populated = {column: cells.get(column, "") for column in "ABCDEFGHIJKLM"}
        if not any(populated.values()):
            continue
        if populated["A"] and not any(populated[column] for column in "BCDEFGHIJKLM"):
            break
        if all(populated[column] == label for column, label in HEADERS.items()):
            header_seen = True
            continue
        if not header_seen:
            raise ValueError(f"Linha {number}: layout inesperado antes do cabeçalho Renda Fixa")
        description = populated["A"]
        if not description:
            raise ValueError(f"Linha {number}: título de renda fixa sem descrição")
        balance_total += decimal_br(populated["B"], number, "saldo a mercado")
        applied = decimal_br(populated["D"], number, "valor aplicado") if populated["D"] else None
        quantity = integer_br(populated["I"], number, "quantidade") if populated["I"] else None
        rentability = populated["F"] if populated["F"] and populated["F"].casefold() not in ("indefinido", "-") else PENDING
        records.append({
            "ticker": description.replace(" ", "_"),
            "description": description,
            "type": classify_rentability_type(rentability),
            "investment_date": iso_date(populated["G"], number, "data aplicação") if populated["G"] else PENDING,
            "due_date": iso_date(populated["H"], number) if populated["H"] else PENDING,
            "quantity": str(quantity) if quantity is not None else PENDING,
            "available": str(quantity) if quantity is not None else PENDING,
            "acquisition_price": str(applied) if applied is not None else PENDING,
            "market_rentability": rentability,
            "isin": PENDING,
            "issuer": parse_issuer(description),
            "investment_type": parse_investment_type(description),
        })
    if not header_seen or not records:
        raise ValueError("Seção Renda Fixa sem cabeçalho ou títulos")
    difference = abs(balance_total - expected_balance)
    rounding_limit = min(Decimal("0.05"), Decimal("0.005") * (len(records) + 1))
    if difference > rounding_limit:
        raise ValueError(f"Total Renda Fixa divergente: linhas={balance_total}, seção={expected_balance}")
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
    def issuer_from_description(record):
        return parse_issuer(record["description"])
    def investment_type_from_description(record):
        return parse_investment_type(record["description"])
    def type_from_rentability(record):
        return classify_rentability_type(record.get("market_rentability", PENDING))
    added, preserved = write_csv(records, OUTPUT, CSV_FIELDS_RF, {
        "isin": PENDING,
        "issuer": issuer_from_description,
        "investment_type": investment_type_from_description,
        "type": type_from_rentability,
    }, pending_updates={
        "issuer": issuer_from_description,
        "investment_type": investment_type_from_description,
        "type": type_from_rentability,
    })
    print(f"{added} título(s) novo(s); {preserved} registro(s) existente(s) preservado(s) em {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, IndexError, OSError, BadZipFile, ET.ParseError) as exc:
        raise SystemExit(f"Erro: {exc}") from exc
