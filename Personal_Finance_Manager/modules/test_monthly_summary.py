import unittest
from unittest.mock import patch
from modules.monthly_summary import MonthlySummary

class TestMonthlySummary(unittest.TestCase):
    def setUp(self):
        self.summary = MonthlySummary()

    @patch.object(MonthlySummary, 'load_transactions')
    def test_month_with_income_and_expense(self, mock_load):
        mock_load.return_value = [
            {'date': '2024-05-10 10:00:00', 'type': 'pemasukan', 'amount': 500000, 'category': 'Gaji'},
            {'date': '2024-05-12 15:30:00', 'type': 'pengeluaran', 'amount': 150000, 'category': 'Makanan'},
            {'date': '2024-05-20 18:00:00', 'type': 'pengeluaran', 'amount': 100000, 'category': 'Transportasi'},
        ]
        result = self.summary.get_monthly_summary(5, 2024)
        self.assertEqual(result['income'], 500000)
        self.assertEqual(result['expense'], 250000)
        self.assertEqual(result['category_expenses'], {'Makanan': 150000, 'Transportasi': 100000})

    @patch.object(MonthlySummary, 'load_transactions')
    def test_month_with_no_transactions(self, mock_load):
        mock_load.return_value = []
        result = self.summary.get_monthly_summary(6, 2024)
        self.assertEqual(result['income'], 0)
        self.assertEqual(result['expense'], 0)
        self.assertEqual(result['category_expenses'], {})

    @patch.object(MonthlySummary, 'load_transactions')
    def test_only_income(self, mock_load):
        mock_load.return_value = [
            {'date': '2024-04-01 09:00:00', 'type': 'pemasukan', 'amount': 200000, 'category': 'Bonus'},
        ]
        result = self.summary.get_monthly_summary(4, 2024)
        self.assertEqual(result['income'], 200000)
        self.assertEqual(result['expense'], 0)
        self.assertEqual(result['category_expenses'], {})

    @patch.object(MonthlySummary, 'load_transactions')
    def test_only_expense(self, mock_load):
        mock_load.return_value = [
            {'date': '2024-04-02 12:00:00', 'type': 'pengeluaran', 'amount': 75000, 'category': 'Hiburan'},
        ]
        result = self.summary.get_monthly_summary(4, 2024)
        self.assertEqual(result['income'], 0)
        self.assertEqual(result['expense'], 75000)
        self.assertEqual(result['category_expenses'], {'Hiburan': 75000})

if __name__ == '__main__':
    unittest.main()
