import unittest

from scripts.xp_import_previdencia import import_rows


class PrevidenciaImportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            (1, {"A": "Previdência Privada", "G": "R$ 175,00"}),
            (2, {"A": "1% | Pós-Fixado", "D": "Saldo", "E": "% Alocação", "F": "Rendimento bruto", "G": "Valor aplicado"}),
            (3, {"A": "Fundo A", "D": "R$ 100,00", "G": "R$ 80,00"}),
            (4, {"A": "Fundo A", "D": "R$ 25,00", "G": "R$ 20,00"}),
            (5, {"A": "1% | Multimercados", "D": "Saldo", "E": "% Alocação", "F": "Rendimento bruto", "G": "Valor aplicado"}),
            (6, {"A": "Fundo B", "D": "R$ 50,00"}),
            (7, {"A": "Fundos Imobiliários", "G": "R$ 10,00"}),
        ]

    def test_keeps_each_fund_row_and_classifies_multimercados(self):
        records = import_rows(self.rows)
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0], {
            "ticker": "Fundo_A",
            "description": "Fundo A",
            "type": "pos",
            "investment_date": "[pending]",
            "due_date": "",
            "quantity": "1",
            "available": "1",
            "acquisition_price": "80.00",
        })
        self.assertEqual(records[1]["ticker"], "Fundo_A_2")
        self.assertEqual(records[1]["acquisition_price"], "20.00")
        self.assertEqual(records[2]["type"], "multi")
        self.assertEqual(records[2]["acquisition_price"], "[pending]")

    def test_missing_applied_value_affects_only_its_own_row(self):
        self.rows[3][1]["G"] = ""
        records = import_rows(self.rows)
        self.assertEqual(records[0]["acquisition_price"], "80.00")
        self.assertEqual(records[1]["acquisition_price"], "[pending]")

    def test_rejects_balance_mismatch(self):
        self.rows[0][1]["G"] = "R$ 174,99"
        with self.assertRaisesRegex(ValueError, "Total Previdência Privada divergente"):
            import_rows(self.rows)

    def test_rejects_missing_id(self):
        self.rows[2][1]["A"] = ""
        with self.assertRaisesRegex(ValueError, "sem descrição"):
            import_rows(self.rows)


if __name__ == "__main__":
    unittest.main()
