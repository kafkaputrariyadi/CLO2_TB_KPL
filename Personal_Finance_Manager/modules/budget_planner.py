import json
import os
import re
from enum import Enum
from typing import List, Dict, Any, TypeVar
from utils.table_utils import display_table

T = TypeVar('T', bound=Dict[str, Any])

class AppState(Enum):
    IDLE = 'idle'
    CREATE = 'create'
    ALERT = 'alert'
    EXIT = 'exit'

class BudgetPlanner:
    """
    Kelas untuk mengelola anggaran dengan validasi input dan penyimpanan aman.
    """

    def __init__(self):  # ✅ Perbaikan: __init__ bukan _init_
        self.data_dir = 'data'
        self.budgets_file = os.path.join(self.data_dir, 'budgets.json')
        self.transactions_file = os.path.join(self.data_dir, 'transactions.json')
        self.state = AppState.IDLE
        os.makedirs(self.data_dir, exist_ok=True)

    def update_field(self, item: T, field: str, value: Any) -> T:
        item[field] = value
        return item

    def load_json_data(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_json_data(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
        except IOError as e:
            print(f"❌ Gagal menyimpan data ke {file_path}: {e}")

    def load_budgets(self) -> List[Dict[str, Any]]:
        return self.load_json_data(self.budgets_file)

    def save_budgets(self, budgets: List[Dict[str, Any]]) -> None:
        self.save_json_data(self.budgets_file, budgets)

    def load_transactions(self) -> List[Dict[str, Any]]:
        return self.load_json_data(self.transactions_file)

    def get_positive_float(self, prompt: str) -> float:
        while True:
            user_input = input(prompt).strip()
            try:
                value = float(user_input)
                if value <= 0:
                    raise ValueError("Angka harus lebih dari 0.")
                return value
            except ValueError:
                print("❌ Masukkan angka yang valid dan lebih dari 0.")

    def get_valid_period(self) -> str:
        while True:
            period = input("Masukkan periode anggaran (bulan/tahun): ").strip().lower()
            if period in ['bulan', 'tahun']:
                return period
            print("❌ Periode harus 'bulan' atau 'tahun'.")

    def is_valid_category(self, category: str, budgets: List[Dict[str, Any]]) -> bool:
        if not re.fullmatch(r"[\w\s\-_,.]{1,50}", category):
            print("❌ Nama kategori tidak valid. Gunakan huruf/angka dan panjang < 50 karakter.")
            return False
        if any(budget['category'].lower() == category.lower() for budget in budgets):
            print("❌ Kategori ini sudah ada.")
            return False
        return True

    def create_budget(self) -> None:
        category = input("Masukkan kategori anggaran: ").strip()
        budgets = self.load_budgets()

        if not self.is_valid_category(category, budgets):
            return

        amount = self.get_positive_float("Masukkan jumlah anggaran: ")
        period = self.get_valid_period()

        new_budget = {
            'category': category,
            'amount': amount,
            'period': period,
            'remaining': amount
        }

        budgets.append(new_budget)
        self.save_budgets(budgets)
        print("✅ Anggaran berhasil dibuat!")
        self.state = AppState.IDLE

    def check_budgets(self) -> List[Dict[str, Any]]:
        budgets = self.load_budgets()
        transactions = self.load_transactions()

        for budget in budgets:
            total_spent = sum(
                trans.get('amount', 0)
                for trans in transactions
                if trans.get('category') == budget.get('category') and trans.get('type') == 'pengeluaran'
            )
            budget['remaining'] = max(0, budget['amount'] - total_spent)

        self.save_budgets(budgets)
        return budgets

    def view_budgets(self) -> None:
        budgets = self.check_budgets()
        if not budgets:
            print("Belum ada anggaran yang dibuat.")
            return

        headers = ["Kategori", "Anggaran", "Terpakai", "Sisa", "Periode"]
        rows = [
            [
                budget['category'],
                f"Rp{budget['amount']:,.2f}",
                f"Rp{budget['amount'] - budget['remaining']:,.2f}",
                f"Rp{budget['remaining']:,.2f}",
                budget['period']
            ]
            for budget in budgets
        ]
        display_table(headers, rows)

    def display_alert(self, budget: Dict[str, Any]) -> None:
        remaining_percent = (budget['remaining'] / budget['amount']) * 100 if budget['amount'] else 0
        if remaining_percent < 0:
            print(f"\n⚠  MELEBIHI ANGGARAN: {budget['category']}")
        elif remaining_percent < 20:
            print(f"\n⚠  MENDESAK: {budget['category']} tinggal {remaining_percent:.1f}%")

    def check_budget_alerts(self) -> None:
        budgets = self.check_budgets()
        for budget in budgets:
            if budget['amount'] == 0:
                continue
            self.display_alert(budget)
        self.state = AppState.IDLE

    def run(self) -> None:
        menu_options = {
            '1': AppState.CREATE,
            '2': AppState.ALERT,
            '9': AppState.EXIT
        }

        while self.state != AppState.EXIT:
            if self.state == AppState.IDLE:
                print(f"\n📊 Menu Anggaran (State: {self.state.value})")
                print("1. Buat Anggaran")
                print("2. Cek Peringatan Anggaran")
                print("9. Keluar")
                choice = input("Pilih: ").strip()
                self.state = menu_options.get(choice, AppState.IDLE)
                if self.state == AppState.IDLE and choice not in menu_options:
                    print("❌ Pilihan tidak valid.")
            elif self.state == AppState.CREATE:
                self.create_budget()
            elif self.state == AppState.ALERT:
                self.view_budgets()
                self.check_budget_alerts()
