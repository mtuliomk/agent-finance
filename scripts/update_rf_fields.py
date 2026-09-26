#!/usr/bin/env python3
"""Update type and investment_type fields in existing renda_fixa.csv based on market_rentability and description."""

import csv
from pathlib import Path

if __package__:
    from .xp_import_rf import CSV_FIELDS_RF, classify_rentability_type, parse_investment_type
else:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from xp_import_rf import CSV_FIELDS_RF, classify_rentability_type, parse_investment_type

ROOT = Path(__file__).parent.parent
OUTPUT = ROOT / "state" / "positions" / "renda_fixa.csv"


def main():
    """Update type and investment_type fields in the existing CSV."""
    if not OUTPUT.exists():
        raise SystemExit(f"Erro: arquivo não encontrado: {OUTPUT}")

    # Read existing records
    with OUTPUT.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        existing_fields = reader.fieldnames
        records = list(reader)

    if not records:
        print("Nenhum registro encontrado no CSV")
        return

    # Check if investment_type field exists, if not add it
    needs_migration = "investment_type" not in existing_fields

    # Update fields
    updated_count = 0
    for record in records:
        old_type = record.get("type", "[pending]")
        old_investment_type = record.get("investment_type", "[pending]")

        # Update type based on market_rentability
        new_type = classify_rentability_type(record.get("market_rentability", "[pending]"))
        if new_type != "[pending]" and (old_type == "variavel" or old_type == "[pending]" or needs_migration):
            record["type"] = new_type
            updated_count += 1

        # Update investment_type based on description
        new_investment_type = parse_investment_type(record.get("description", ""))
        if needs_migration or old_investment_type == "[pending]":
            record["investment_type"] = new_investment_type
            if new_investment_type != "[pending]":
                updated_count += 1

    # Write updated records
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS_RF)
        writer.writeheader()
        writer.writerows(records)

    print(f"✓ Atualizado {updated_count} campo(s) em {len(records)} registro(s)")
    print(f"  • Arquivo: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"Erro: {exc}") from exc
