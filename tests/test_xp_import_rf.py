import csv
import tempfile
import unittest
from pathlib import Path

from scripts.xp_import_position import write_csv
from scripts.xp_import_rf import CSV_FIELDS_RF, import_rows, parse_issuer, parse_investment_type, classify_rentability_type


class RendaFixaImportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            (1, {"A": "Renda Fixa", "G": "R$ 150,00"}),
            (2, {"A": "1% | Inflação", "B": "Saldo a mercado", "C": "% Alocação", "D": "Valor aplicado", "E": "Valor aplicado original", "F": "Rentabilidade a mercado", "G": "Data aplicação", "H": "Data vencimento", "I": "Quantidade", "J": "Preço Unitário", "K": "IR", "L": "IOF", "M": "Saldo líquido"}),
            (3, {"A": "CDB A - FEV/2028", "B": "R$ 100,00", "D": "R$ 80,00", "F": "IPC-A +5,35%", "G": "01/02/2024", "H": "01/02/2028", "I": "1"}),
            (4, {"A": "CDB A - FEV/2028", "B": "R$ 50,00", "D": "R$ 40,00", "F": "10,5% a.a.", "G": "02/02/2024", "H": "02/02/2028", "I": "20"}),
            (5, {"A": "Dividendos, proventos e outras distribuições"}),
            (6, {"A": "Ações", "G": "R$ 10,00"}),
        ]

    def test_imports_each_lot_with_sequential_id_and_extra_column(self):
        records = import_rows(self.rows)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0], {
            "ticker": "CDB_A_-_FEV/2028",
            "description": "CDB A - FEV/2028",
            "type": "ipca",
            "investment_date": "2024-02-01",
            "due_date": "2028-02-01",
            "quantity": "1",
            "available": "1",
            "acquisition_price": "80.00",
            "market_rentability": "IPC-A +5,35%",
            "isin": "[pending]",
            "issuer": "A",
            "investment_type": "CDB",
        })
        self.assertEqual(records[1]["ticker"], "CDB_A_-_FEV/2028_2")
        self.assertEqual(records[1]["type"], "pre")
        self.assertEqual(records[1]["isin"], "[pending]")
        self.assertEqual(records[1]["issuer"], "A")
        self.assertEqual(records[1]["investment_type"], "CDB")
        self.assertEqual(records[1]["quantity"], "20")
        self.assertEqual(records[1]["available"], "20")
        self.assertEqual(records[1]["acquisition_price"], "40.00")

    def test_missing_source_fields_are_pending(self):
        for column in "DFGHI":
            self.rows[2][1][column] = ""
        record = import_rows(self.rows)[0]
        self.assertEqual([record[field] for field in ("investment_date", "due_date", "quantity", "available", "acquisition_price", "market_rentability", "isin")], ["[pending]"] * 7)

    def test_accepts_small_display_rounding_difference(self):
        self.rows[0][1]["G"] = "R$ 150,01"
        self.assertEqual(len(import_rows(self.rows)), 2)

    def test_rejects_material_balance_difference(self):
        self.rows[0][1]["G"] = "R$ 150,10"
        with self.assertRaisesRegex(ValueError, "Total Renda Fixa divergente"):
            import_rows(self.rows)

    def test_parses_displayed_name_from_description(self):
        examples = {
            "CDB AGIBANK - JUL/2027": "AGIBANK",
            "CDB PINE - JURO MENSAL - JUL/2027": "PINE",
            "CDB MIDWAY - RIACHUELO S.A. - JAN/2028": "MIDWAY - RIACHUELO S.A.",
            "LCA BANCO BV S/A - JURO MENSAL - SET/2027": "BANCO BV S/A",
            "LCD BNDES - JUL/2032": "BNDES",
            "LF BANCO BV S/A - JUN/2027": "BANCO BV S/A",
            "DEB VIA BRASIL BR 163 - DEZ/2030": "VIA BRASIL BR 163",
            "CRA BRF - MAI/2031": "BRF",
            "CRI DASA - JAN/2029": "DASA",
            "CRI BROOKFIELD - FL SQUARE - ABR/2027": "BROOKFIELD - FL SQUARE",
            "FND CREDITAS - OUT/2027": "CREDITAS",
            "CDB AGIBANK sem vencimento": "[pending]",
        }
        for description, expected in examples.items():
            with self.subTest(description=description):
                self.assertEqual(parse_issuer(description), expected)

    def test_parses_investment_type_from_description(self):
        examples = {
            "CDB AGIBANK - JUL/2027": "CDB",
            "LCA BANCO BV S/A - JURO MENSAL - SET/2027": "LCA",
            "LCD BNDES - JUL/2032": "LCD",
            "LF BANCO BV S/A - JUN/2027": "LF",
            "DEB VIA BRASIL BR 163 - DEZ/2030": "DEB",
            "CRA BRF - MAI/2031": "CRA",
            "CRI DASA - JAN/2029": "CRI",
            "FND CREDITAS - OUT/2027": "FND",
            "CDB AGIBANK sem vencimento": "[pending]",
        }
        for description, expected in examples.items():
            with self.subTest(description=description):
                self.assertEqual(parse_investment_type(description), expected)

    def test_classifies_rentability_type(self):
        examples = {
            "IPC-A +5,35%": "ipca",
            "IPCA +5,35%": "ipca",
            "+14,01%": "pre",
            "+15,40%": "pre",
            "96,00% CDI": "pos",
            "CDI +1,85%": "pos",
            "118,00% CDI": "pos",
            "10,5% a.a.": "pre",
            "11,2% a.m.": "pre",
            "indefinido": "[pending]",
            "-": "[pending]",
            "": "[pending]",
        }
        for rentability, expected in examples.items():
            with self.subTest(rentability=rentability):
                self.assertEqual(classify_rentability_type(rentability), expected)

    def test_extra_column_is_written_and_repeat_import_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "renda_fixa.csv"
            records = import_rows(self.rows)
            self.assertEqual(write_csv(records, output, CSV_FIELDS_RF), (2, 0))
            before = output.read_bytes()
            with output.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, list(CSV_FIELDS_RF))
                saved = list(reader)
            self.assertEqual(saved[0]["market_rentability"], "IPC-A +5,35%")
            self.assertEqual(saved[0]["type"], "ipca")
            self.assertEqual(saved[1]["type"], "pre")
            self.assertTrue(all(record["isin"] == "[pending]" for record in saved))
            self.assertTrue(all(record["issuer"] == "A" for record in saved))
            self.assertTrue(all(record["investment_type"] == "CDB" for record in saved))
            self.assertEqual(write_csv(records, output, CSV_FIELDS_RF), (0, 2))
            self.assertEqual(output.read_bytes(), before)

    def test_reimport_fills_only_pending_issuer_in_existing_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "renda_fixa.csv"
            records = import_rows(self.rows)
            existing = [dict(record) for record in records]
            existing[0]["description"] = "CRI DASA - JAN/2029"
            existing[0]["ticker"] = "CRI_DASA_-_JAN/2029"
            existing[0]["issuer"] = "[pending]"
            existing[1]["description"] = "CRA BRF - MAI/2031"
            existing[1]["ticker"] = "CRA_BRF_-_MAI/2031"
            existing[1]["issuer"] = "Valor manual"
            with output.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS_RF)
                writer.writeheader()
                writer.writerows(existing)

            update = {"issuer": lambda record: parse_issuer(record["description"])}
            self.assertEqual(write_csv(existing, output, CSV_FIELDS_RF, pending_updates=update), (0, 2))
            with output.open(newline="", encoding="utf-8") as handle:
                saved = list(csv.DictReader(handle))
            self.assertEqual([record["issuer"] for record in saved], ["DASA", "Valor manual"])
            before = output.read_bytes()
            self.assertEqual(write_csv(existing, output, CSV_FIELDS_RF, pending_updates=update), (0, 2))
            self.assertEqual(output.read_bytes(), before)

    def test_migrates_previous_headers_without_changing_existing_fields(self):
        for missing_count in (1, 2):
            with self.subTest(missing_count=missing_count), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "renda_fixa.csv"
                records = import_rows(self.rows)
                legacy_fields = CSV_FIELDS_RF[:-missing_count]
                legacy_records = [{field: record[field] for field in legacy_fields} for record in records]
                if "isin" in legacy_fields:
                    legacy_records[0]["isin"] = "BRTEST000001"
                with output.open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=legacy_fields)
                    writer.writeheader()
                    writer.writerows(legacy_records)

                defaults = {
                    "isin": "[pending]",
                    "issuer": lambda record: parse_issuer(record["description"]),
                    "investment_type": lambda record: parse_investment_type(record["description"]),
                    "type": lambda record: classify_rentability_type(record.get("market_rentability", "[pending]")),
                }
                self.assertEqual(write_csv(records, output, CSV_FIELDS_RF, defaults), (0, 2))
                with output.open(newline="", encoding="utf-8") as handle:
                    reader = csv.DictReader(handle)
                    self.assertEqual(reader.fieldnames, list(CSV_FIELDS_RF))
                    migrated = list(reader)
                self.assertEqual(
                    [{field: record[field] for field in legacy_fields} for record in migrated],
                    legacy_records,
                )
                self.assertTrue(all(record["issuer"] == "A" for record in migrated))
                if "isin" not in legacy_fields:
                    self.assertTrue(all(record["isin"] == "[pending]" for record in migrated))
                before = output.read_bytes()
                self.assertEqual(write_csv(records, output, CSV_FIELDS_RF, defaults), (0, 2))
                self.assertEqual(output.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
