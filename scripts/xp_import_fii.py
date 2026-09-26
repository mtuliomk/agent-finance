#!/usr/bin/env python3
"""Import the Fundos Imobiliários section of one XP PosicaoDetalhada workbook."""

import argparse
import re
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

if __package__:
    from .xp_import_position import INBOX, PENDING, ROOT, decimal_br, read_sheet, write_csv
else:
    from xp_import_position import INBOX, PENDING, ROOT, decimal_br, read_sheet, write_csv

OUTPUT = ROOT / "state" / "positions" / "fundos_imobiliarios.csv"
SECTION = "Fundos Imobiliários"
HEADERS = {
    "B": "Saldo", "C": "% Alocação", "D": "Preço médio (abertura)",
    "E": "Última cotação", "F": "Qtd. total", "G": "Quantidade de Cotas",
}


def integer_br(value, row_number, field):
    if not re.fullmatch(r"(?:\d{1,3}(?:\.\d{3})+|\d+)", value):
        raise ValueError(f"Linha {row_number}: {field} inválido: {value!r}")
    return int(value.replace(".", ""))


def import_rows(rows):
    markers = [(index, number, cells) for index, (number, cells) in enumerate(rows) if cells.get("A", "").casefold() == SECTION.casefold()]
    if len(markers) != 1:
        raise ValueError(f"A seção {SECTION!r} não foi encontrada exatamente uma vez")
    start, section_line, marker = markers[0]
    expected_balance = decimal_br(marker.get("G", ""), section_line, "total Fundos Imobiliários")
    header_seen = False
    balance_total = Decimal(0)
    records = []
    seen_tickers = set()
    for number, cells in rows[start + 1:]:
        populated = {column: cells.get(column, "") for column in "ABCDEFG"}
        if not any(populated.values()):
            continue
        if populated["A"] and not any(populated[col] for col in "BCDEF") and populated["G"].startswith("R$"):
            break
        if all(populated[col] == label for col, label in HEADERS.items()):
            header_seen = True
            continue
        if not header_seen:
            raise ValueError(f"Linha {number}: layout inesperado antes do cabeçalho Fundos Imobiliários")
        description = populated["A"]
        if not description:
            raise ValueError(f"Linha {number}: FII sem ticker")
        ticker = description.replace(" ", "_")
        if ticker in seen_tickers:
            raise ValueError(f"Linha {number}: ticker FII duplicado: {ticker!r}")
        seen_tickers.add(ticker)
        balance_total += decimal_br(populated["B"], number, "saldo")
        price = decimal_br(populated["D"], number, "preço médio") if populated["D"] and populated["D"].casefold() != "indefinido" else None
        quantity = integer_br(populated["F"], number, "quantidade total") if populated["F"] else None
        available = integer_br(populated["G"], number, "quantidade de cotas") if populated["G"] else None
        if quantity is not None and available is not None and available > quantity:
            raise ValueError(f"Linha {number}: quantidade de cotas maior que a quantidade total")
        records.append({
            "ticker": ticker,
            "description": description,
            "type": "variavel",
            "investment_date": PENDING,
            "due_date": "",
            "quantity": str(quantity) if quantity is not None else PENDING,
            "available": str(available) if available is not None else PENDING,
            "acquisition_price": str(price) if price is not None else PENDING,
        })
    if not header_seen or not records:
        raise ValueError("Seção Fundos Imobiliários sem cabeçalho ou fundos")
    if balance_total != expected_balance:
        raise ValueError(f"Total Fundos Imobiliários divergente: linhas={balance_total}, seção={expected_balance}")
    return records


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
    print(f"{added} FII(s) novo(s); {preserved} registro(s) existente(s) preservado(s) em {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, IndexError, OSError, BadZipFile, ET.ParseError) as exc:
        raise SystemExit(f"Erro: {exc}") from exc
