import unittest

from scripts.xp_import_fii import import_rows


class FiiImportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            (1, {"A": "Fundos Imobiliários", "G": "R$ 105,00"}),
            (2, {"A": "1% | Fundos Listados", "B": "Saldo", "C": "% Alocação", "D": "Preço médio (abertura)", "E": "Última cotação", "F": "Qtd. total", "G": "Quantidade de Cotas"}),
            (3, {"A": "ABC11", "B": "R$ 100,00", "D": "R$ 10,07", "F": "3.000", "G": "2.900"}),
            (4, {"A": "DEF11", "B": "R$ 5,00", "D": "Indefinido", "F": "0", "G": "0"}),
            (5, {"A": "Ações", "G": "R$ 200,00"}),
        ]

    def test_imports_unique_tickers_and_source_columns(self):
        records = import_rows(self.rows)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0], {
            "ticker": "ABC11",
            "description": "ABC11",
            "type": "variavel",
            "investment_date": "[pending]",
            "due_date": "",
            "quantity": "3000",
            "available": "2900",
            "acquisition_price": "10.07",
        })
        self.assertEqual(records[1]["quantity"], "0")
        self.assertEqual(records[1]["available"], "0")
        self.assertEqual(records[1]["acquisition_price"], "[pending]")

    def test_rejects_duplicate_ticker(self):
        self.rows[3][1]["A"] = "ABC11"
        with self.assertRaisesRegex(ValueError, "ticker FII duplicado"):
            import_rows(self.rows)

    def test_rejects_balance_mismatch(self):
        self.rows[0][1]["G"] = "R$ 104,99"
        with self.assertRaisesRegex(ValueError, "Total Fundos Imobiliários divergente"):
            import_rows(self.rows)

    def test_rejects_cotas_above_total(self):
        self.rows[2][1]["G"] = "3.001"
        with self.assertRaisesRegex(ValueError, "maior que a quantidade total"):
            import_rows(self.rows)


if __name__ == "__main__":
    unittest.main()
