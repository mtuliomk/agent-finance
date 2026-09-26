import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import xp_import_position
from scripts.xp_import_position import import_rows


class TesouroDiretoImportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            (1, {"A": "Tesouro Direto", "G": "R$ 125,00"}),
            (2, {"A": "2,1% | Pós-Fixado", "B": "Saldo", "C": "% Alocação", "D": "Valor aplicado", "E": "Quantidade", "F": "Disponível", "G": "Vencimento"}),
            (3, {"A": "NTN-B1 dez/2031", "B": "R$ 100,00", "D": "R$ 100,00", "E": "16,84", "F": "15,84", "G": "15/12/2031"}),
            (4, {"A": "LTN jan/2029", "B": "R$ 25,00", "D": "R$ 25,00", "E": "2,81", "F": "2,81", "G": "01/01/2029"}),
            (5, {}),
            (6, {"A": "Previdência Privada", "G": "R$ 999,00"}),
        ]

    def test_reads_only_tesouro_and_classifies_by_title(self):
        imported = import_rows(self.rows)
        self.assertEqual([record["type"] for record in imported], ["ipca", "pre"])
        self.assertEqual(imported[0]["ticker"], "NTN-B1_dez/2031")
        self.assertEqual(imported[0]["due_date"], "2031-12-15")
        self.assertEqual(imported[0]["quantity"], "16.84")
        self.assertEqual(imported[0]["available"], "15.84")
        self.assertEqual(imported[0]["investment_date"], "[pending]")
        self.assertEqual(imported[0]["acquisition_price"], "[pending]")

    def test_rejects_total_mismatch_instead_of_publishing_partial_data(self):
        self.rows[0][1]["G"] = "R$ 124,99"
        with self.assertRaisesRegex(ValueError, "Total Tesouro Direto divergente"):
            import_rows(self.rows)

    def test_marks_unknown_type_as_pending(self):
        self.rows[2][1]["A"] = "Título desconhecido"
        imported = import_rows(self.rows)
        self.assertEqual(imported[0]["type"], "[pending]")

    def test_marks_missing_fields_as_pending_without_losing_valid_zero(self):
        self.rows[2][1]["E"] = ""
        self.rows[2][1]["F"] = "0"
        self.rows[2][1]["G"] = ""
        imported = import_rows(self.rows)
        self.assertEqual(imported[0]["quantity"], "[pending]")
        self.assertEqual(imported[0]["available"], "0")
        self.assertEqual(imported[0]["due_date"], "[pending]")

    def test_rejects_missing_id(self):
        self.rows[2][1]["A"] = ""
        with self.assertRaisesRegex(ValueError, "sem descrição"):
            import_rows(self.rows)

    def test_duplicate_id_in_source_gets_sequential_ticker(self):
        self.rows[0][1]["G"] = "R$ 150,00"
        self.rows.insert(4, (5, {"A": "LTN jan/2029", "B": "R$ 25,00", "E": "9", "F": "9"}))
        imported = import_rows(self.rows)
        self.assertEqual([record["ticker"] for record in imported], ["NTN-B1_dez/2031", "LTN_jan/2029", "LTN_jan/2029_2"])
        self.assertEqual(imported[1]["quantity"], "2.81")
        self.assertEqual(imported[2]["quantity"], "9")

    def test_sequential_ticker_skips_id_derived_from_other_description(self):
        self.rows[0][1]["G"] = "R$ 200,00"
        self.rows[4:4] = [
            (5, {"A": "LTN jan/2029", "B": "R$ 25,00", "E": "1", "F": "1"}),
            (6, {"A": "LTN jan/2029", "B": "R$ 25,00", "E": "2", "F": "2"}),
            (7, {"A": "LTN jan/2029 2", "B": "R$ 25,00", "E": "3", "F": "3"}),
        ]
        imported = import_rows(self.rows)
        self.assertEqual([record["ticker"] for record in imported], [
            "NTN-B1_dez/2031", "LTN_jan/2029", "LTN_jan/2029_3", "LTN_jan/2029_4", "LTN_jan/2029_2",
        ])

    def test_duplicate_from_new_source_is_appended_without_changing_existing_id(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tesouro_direto.csv"
            with patch.object(xp_import_position, "OUTPUT", output):
                self.assertEqual(xp_import_position.write_csv(import_rows(self.rows)), (2, 0))
                before = output.read_bytes()
                self.rows[0][1]["G"] = "R$ 150,00"
                self.rows.insert(4, (5, {"A": "LTN jan/2029", "B": "R$ 25,00", "E": "9", "F": "9"}))
                imported = import_rows(self.rows)
                self.assertEqual(xp_import_position.write_csv(imported), (1, 2))
                with output.open(newline="", encoding="utf-8") as handle:
                    saved = list(csv.DictReader(handle))
                self.assertEqual(saved[2]["ticker"], "LTN_jan/2029_2")
                self.assertEqual(saved[2]["quantity"], "9")
                after = output.read_bytes()
                self.assertNotEqual(after, before)
                self.assertEqual(xp_import_position.write_csv(imported), (0, 3))
                self.assertEqual(output.read_bytes(), after)

    def test_existing_id_is_preserved_and_repeat_import_does_not_rewrite_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tesouro_direto.csv"
            with patch.object(xp_import_position, "OUTPUT", output):
                first_import = import_rows(self.rows)
                self.assertEqual(xp_import_position.write_csv(first_import), (2, 0))
                with output.open(newline="", encoding="utf-8") as handle:
                    saved = list(csv.DictReader(handle))
                saved[0]["investment_date"] = "2024-05-10"
                saved[0]["acquisition_price"] = "10.50"
                with output.open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=xp_import_position.CSV_FIELDS)
                    writer.writeheader()
                    writer.writerows(saved)
                before = output.read_bytes()
                self.rows[2][1]["E"] = "99"
                self.rows[2][1]["F"] = "99"
                self.assertEqual(xp_import_position.write_csv(import_rows(self.rows)), (0, 2))
                self.assertEqual(output.read_bytes(), before)

                self.rows[0][1]["G"] = "R$ 175,00"
                self.rows.insert(4, (5, {"A": "LFT mar/2030", "B": "R$ 50,00", "E": "1", "F": "1"}))
                self.assertEqual(xp_import_position.write_csv(import_rows(self.rows)), (1, 2))
                with output.open(newline="", encoding="utf-8") as handle:
                    updated = list(csv.DictReader(handle))
                self.assertEqual(updated[:2], saved)
                self.assertEqual(updated[2]["ticker"], "LFT_mar/2030")
                self.assertEqual(updated[2]["investment_date"], "[pending]")

    def test_rejects_duplicate_id_in_existing_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tesouro_direto.csv"
            with patch.object(xp_import_position, "OUTPUT", output):
                self.assertEqual(xp_import_position.write_csv(import_rows(self.rows)), (2, 0))
                with output.open("a", encoding="utf-8") as handle:
                    handle.write("LTN_jan/2029,LTN jan/2029,pre,[pending],2029-01-01,2.81,2.81,[pending]\n")
                with self.assertRaisesRegex(ValueError, "ID ausente/duplicado"):
                    xp_import_position.write_csv(import_rows(self.rows))


if __name__ == "__main__":
    unittest.main()
