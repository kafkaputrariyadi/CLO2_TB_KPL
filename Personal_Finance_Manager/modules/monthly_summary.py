import json
from datetime import datetime
from utils.table_utils import display_table

class MonthlySummary:
    def __init__(self):
        self.transactions_file = 'data/transactions.json'

    def load_transactions(self):
        try:
            with open(self.transactions_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_monthly_summary(self, month, year):
        transactions = self.load_transactions()
        month_str = f"{year}-{month:02d}"
        
        income = 0
        expense = 0
        category_expenses = {}

        for t in transactions:
            t_date = datetime.strptime(t['date'], '%Y-%m-%d %H:%M:%S')
            if t_date.year == year and t_date.month == month:
                if t['type'] == 'pemasukan':
                    income += t['amount']
                else:
                    expense += t['amount']
                    category_expenses[t['category']] = category_expenses.get(t['category'], 0) + t['amount']

        return {
            'income': income,
            'expense': expense,
            'category_expenses': category_expenses
        }

    def show_summary(self):
        month = int(input("Masukkan bulan (1-12): "))
        year = int(input("Masukkan tahun: "))
        
        current = self.get_monthly_summary(month, year)
        previous_month = month - 1 if month > 1 else 12
        previous_year = year if month > 1 else year - 1
        previous = self.get_monthly_summary(previous_month, previous_year)

        print(f"\nRingkasan Bulan {month}/{year}:")
        print(f"Total Pemasukan: Rp{current['income']:,.2f}")
        print(f"Total Pengeluaran: Rp{current['expense']:,.2f}")
        print(f"Saldo: Rp{current['income'] - current['expense']:,.2f}")

        print("\nPerbandingan dengan Bulan Sebelumnya:")
        income_diff = current['income'] - previous['income']
        expense_diff = current['expense'] - previous['expense']
        print(f"Perbedaan Pemasukan: {'+' if income_diff >=0 else ''}{income_diff:,.2f}")
        print(f"Perbedaan Pengeluaran: {'+' if expense_diff >=0 else ''}{expense_diff:,.2f}")

        print("\nPengeluaran per Kategori:")
        headers = ["Kategori", "Jumlah"]
        rows = [[k, f"Rp{v:,.2f}"] for k, v in current['category_expenses'].items()]
        display_table(headers, rows)

    def run(self):
        while True:
            print("\nRingkasan Keuangan Bulanan:")
            print("1. Menampilkan total pemasukan dan pengeluaran bulanan")
            print("2. Menampilkan perbandingan sederhana dengan bulan sebelumnya")
            print("9. Kembali")
            
            choice = input("Pilih menu: ")
            
            if choice == '1':
                self.show_summary()
            elif choice == '2':
                self.show_summary() 
            elif choice == '9':
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

