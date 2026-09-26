import csv
import tempfile
import unittest
from pathlib import Path

from scripts.xp_import_position import write_csv
from scripts.xp_import_rf import CSV_FIELDS_RF, import_rows


class RendaFixaImportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            (1, {"A": "Renda Fixa", "G": "R$ 150,00"}),
            (2, {"A": "1% | Inflação", "B": "Saldo a mercado", "C": "% Alocação", "D": "Valor aplicado", "E": "Valor aplicado original", "F": "Rentabilidade a mercado", "G": "Data aplicação", "H": "Data vencimento", "I": "Quantidade", "J": "Preço Unitário", "K": "IR", "L": "IOF", "M": "Saldo líquido"}),
            (3, {"A": "CDB A", "B": "R$ 100,00", "D": "R$ 80,00", "F": "IPC-A +5,35%", "G": "01/02/2024", "H": "01/02/2028", "I": "1"}),
            (4, {"A": "CDB A", "B": "R$ 50,00", "D": "R$ 40,00", "F": "10,5% a.a.", "G": "02/02/2024", "H": "02/02/2028", "I": "20"}),
            (5, {"A": "Dividendos, proventos e outras distribuições"}),
            (6, {"A": "Ações", "G": "R$ 10,00"}),
        ]

    def test_imports_each_lot_with_sequential_id_and_extra_column(self):
        records = import_rows(self.rows)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0], {
            "ticker": "CDB_A",
            "description": "CDB A",
            "type": "variavel",
            "investment_date": "2024-02-01",
            "due_date": "2028-02-01",
            "quantity": "1",
            "available": "1",
            "acquisition_price": "80.00",
            "market_rentability": "IPC-A +5,35%",
            "isin": "[pending]",
        })
        self.assertEqual(records[1]["ticker"], "CDB_A_2")
        self.assertEqual(records[1]["isin"], "[pending]")
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
            self.assertTrue(all(record["isin"] == "[pending]" for record in saved))
            self.assertEqual(write_csv(records, output, CSV_FIELDS_RF), (0, 2))
            self.assertEqual(output.read_bytes(), before)

    def test_adds_isin_to_existing_csv_without_changing_other_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "renda_fixa.csv"
            records = import_rows(self.rows)
            legacy_fields = CSV_FIELDS_RF[:-1]
            legacy_records = [{field: record[field] for field in legacy_fields} for record in records]
            with output.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=legacy_fields)
                writer.writeheader()
                writer.writerows(legacy_records)

            self.assertEqual(write_csv(records, output, CSV_FIELDS_RF, {"isin": "[pending]"}), (0, 2))
            with output.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, list(CSV_FIELDS_RF))
                migrated = list(reader)
            self.assertEqual(
                [{field: record[field] for field in legacy_fields} for record in migrated],
                legacy_records,
            )
            self.assertTrue(all(record["isin"] == "[pending]" for record in migrated))
            before = output.read_bytes()
            self.assertEqual(write_csv(records, output, CSV_FIELDS_RF, {"isin": "[pending]"}), (0, 2))
            self.assertEqual(output.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
