import json
from utils.table_utils import display_table

class BudgetPlanner:
    def __init__(self):
        self.budgets_file = 'data/budgets.json'
        self.transactions_file = 'data/transactions.json'
        self.state = 'idle'  

    def load_budgets(self):
        try:
            with open(self.budgets_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_budgets(self, budgets):
        with open(self.budgets_file, 'w') as f:
            json.dump(budgets, f, indent=2)

    def load_transactions(self):
        try:
            with open(self.transactions_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def create_budget(self):
        category = input("Masukkan kategori anggaran: ")
        amount = float(input("Masukkan jumlah anggaran: "))
        period = input("Masukkan periode anggaran (bulan/tahun): ").lower()

        budget = {
            'category': category,
            'amount': amount,
            'period': period,
            'remaining': amount
        }

        budgets = self.load_budgets()
        budgets.append(budget)
        self.save_budgets(budgets)
        print("Anggaran berhasil dibuat!")

    def check_budgets(self):
        budgets = self.load_budgets()
        transactions = self.load_transactions()

        for budget in budgets:
            total_spent = sum(
                t['amount'] for t in transactions 
                if t['category'] == budget['category'] and t['type'] == 'pengeluaran'
            )
            budget['remaining'] = budget['amount'] - total_spent

        self.save_budgets(budgets)
        return budgets

    def view_budgets(self):
        budgets = self.check_budgets()
        if not budgets:
            print("Belum ada anggaran yang dibuat.")
            return

        headers = ["Kategori", "Anggaran", "Terpakai", "Sisa", "Periode"]
        rows = []
        for b in budgets:
            spent = b['amount'] - b['remaining']
            rows.append([
                b['category'],
                f"Rp{b['amount']:,.2f}",
                f"Rp{spent:,.2f}",
                f"Rp{b['remaining']:,.2f}",
                b['period']
            ])
        
        display_table(headers, rows)

    def run(self):
        while True:
            print("\nPerencanaan dan Pemantauan Anggaran:")
            print("1. Pembuatan anggaran per kategori")
            print("2. Peringatan ketika pengeluaran mendekati atau melebihi batas anggaran")
            print("9. Kembali")
            
            choice = input("Pilih menu: ")
            
            if choice == '1':
                self.create_budget()
            elif choice == '2':
                self.view_budgets()
                self.check_budget_alerts()
            elif choice == '9':
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    def check_budget_alerts(self):
        budgets = self.check_budgets()
        for budget in budgets:
            remaining_percent = (budget['remaining'] / budget['amount']) * 100
            if remaining_percent < 0:
                print(f"\nPERINGATAN: Pengeluaran untuk kategori {budget['category']} melebihi anggaran!")
            elif remaining_percent < 20:
                print(f"\nPERINGATAN: Pengeluaran untuk kategori {budget['category']} mendekati batas anggaran (sisa {remaining_percent:.1f}%)")