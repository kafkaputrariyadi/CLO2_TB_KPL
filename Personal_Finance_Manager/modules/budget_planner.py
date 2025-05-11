import json
from typing import List, Dict, Any, TypeVar
from utils.table_utils import display_table

T = TypeVar('T', bound=Dict[str, Any])

class BudgetPlanner:
    def __init__(self):
        self.budgets_file = 'data/budgets.json'
        self.transactions_file = 'data/transactions.json'
        self.state = 'idle' 

    def update_field(self, item: T, field: str, value: Any) -> T:
        item[field] = value
        return item

    def load_budgets(self) -> List[Dict[str, Any]]:
        try:
            with open(self.budgets_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_budgets(self, budgets: List[Dict[str, Any]]):
        with open(self.budgets_file, 'w') as f:
            json.dump(budgets, f, indent=2)

    def load_transactions(self) -> List[Dict[str, Any]]:
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
        print("✅ Anggaran berhasil dibuat!")

        self.state = 'idle'  

    def check_budgets(self) -> List[Dict[str, Any]]:
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

    def check_budget_alerts(self):
        budgets = self.check_budgets()
        for budget in budgets:
            remaining_percent = (budget['remaining'] / budget['amount']) * 100
            if remaining_percent < 0:
                print(f"\n⚠️  MELEBIHI ANGGARAN: {budget['category']}")
            elif remaining_percent < 20:
                print(f"\n⚠️  MENDESAK: {budget['category']} tinggal {remaining_percent:.1f}%")
        self.state = 'idle'

    def run(self):
        while self.state != 'exit':
            if self.state == 'idle':
                print("\n Menu Anggaran (State:", self.state, ")")
                print("1. Buat Anggaran")
                print("2. Cek Peringatan Anggaran")
                print("9. Keluar")
                pilihan = input("Pilih: ")

                if pilihan == '1':
                    self.state = 'create'
                elif pilihan == '2':
                    self.state = 'alert'
                elif pilihan == '9':
                    self.state = 'exit'
                else:
                    print("❌ Pilihan tidak valid.")
            elif self.state == 'create':
                self.create_budget()
            elif self.state == 'alert':
                self.view_budgets()
                self.check_budget_alerts()
