import unittest

from scripts.xp_import_acoes import import_rows


class AcoesImportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            (1, {"A": "Ações", "G": "R$ 105,00"}),
            (2, {"A": "1% | Renda Variável Brasil", "B": "Saldo", "C": "% Alocação", "D": "Rentabilidade", "E": "Preço médio", "F": "Último preço (R$)", "G": "Qtd. total"}),
            (3, {"A": "ABC3", "B": "R$ 100,00", "E": "R$ 10,07", "G": "3.000"}),
            (4, {"A": "DEF4", "B": "R$ 5,00", "E": "Indefinido", "G": "0"}),
            (5, {"A": "Renda Fixa", "G": "R$ 200,00"}),
            (6, {"A": "Ações", "G": "R$ 9,00"}),
            (7, {"A": "1% | Renda Variável Brasil", "B": "Provisionado", "C": "% Alocação", "D": "Valor provisionado bruto", "E": "Valor provisionado líquido", "F": "Evento", "G": "Previsão pagamento"}),
        ]

    def test_imports_unique_tickers_and_source_columns(self):
        records = import_rows(self.rows)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0], {
            "ticker": "ABC3",
            "description": "ABC3",
            "type": "variavel",
            "investment_date": "[pending]",
            "due_date": "",
            "quantity": "3000",
            "available": "3000",
            "acquisition_price": "10.07",
        })
        self.assertEqual(records[1]["quantity"], "0")
        self.assertEqual(records[1]["available"], "0")
        self.assertEqual(records[1]["acquisition_price"], "[pending]")

    def test_rejects_duplicate_ticker(self):
        self.rows[3][1]["A"] = "ABC3"
        with self.assertRaisesRegex(ValueError, "ticker de ação duplicado"):
            import_rows(self.rows)

    def test_rejects_balance_mismatch(self):
        self.rows[0][1]["G"] = "R$ 104,99"
        with self.assertRaisesRegex(ValueError, "Total Ações divergente"):
            import_rows(self.rows)

    def test_missing_quantity_is_pending(self):
        self.rows[2][1]["G"] = ""
        record = import_rows(self.rows)[0]
        self.assertEqual(record["quantity"], "[pending]")
        self.assertEqual(record["available"], "[pending]")


if __name__ == "__main__":
    unittest.main()
