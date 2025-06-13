import json
import re
from datetime import datetime
from utils.table_utils import display_table

class TransactionRecorder:
    CATEGORIES = {
        '1': 'Makanan',
        '2': 'Transportasi',
        '3': 'Hiburan',
        '4': 'Perumahan',
        '5': 'Kesehatan',
        '6': 'Pendidikan',
        '7': 'Lainnya'
    }

    def __init__(self, transactions_file='data/transactions.json'):
        self.transactions_file = transactions_file

    def load_transactions(self):
        try:
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
           
            return []
        except json.JSONDecodeError:
            print("File data transaksi rusak atau tidak valid. Menggunakan data kosong.")
            return []

    def save_transaction(self, transactions):
        try:
            with open(self.transactions_file, 'w', encoding='utf-8') as f:
                json.dump(transactions, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Gagal menyimpan data transaksi: {e}")

    def input_amount(self, transaction_type):
        while True:
            try:
                value = input(f"Masukkan jumlah {transaction_type} (misal: 15000 atau 15000.50): ").strip()
                if not re.match(r'^\d+(\.\d{1,2})?$', value):
                    raise ValueError("Format angka tidak valid. Gunakan angka positif dengan maksimal 2 desimal.")
                amount = float(value)
                if amount <= 0:
                    raise ValueError("Jumlah harus lebih besar dari nol.")
                return amount
            except ValueError as e:
                print(f"Input salah: {e}")

    def input_description(self):
        while True:
            desc = input("Masukkan deskripsi (maks 100 karakter, hanya huruf, angka, spasi, .,,-): ").strip()
            if 0 < len(desc) <= 100:
                if not re.match(r'^[\w\s.,-]*$', desc):
                    print("Deskripsi mengandung karakter tidak valid. Coba lagi.")
                    continue
                return desc
            else:
                print("Deskripsi harus diisi dan maksimal 100 karakter.")

    def input_category(self):
        while True:
            print("\nKategori:")
            for num, cat in self.CATEGORIES.items():
                print(f"{num}. {cat}")
            choice = input("Pilih kategori: ").strip()
            if choice in self.CATEGORIES:
                return self.CATEGORIES[choice]
            else:
                print("Kategori tidak valid, silakan pilih lagi.")

    def record_transaction(self, transaction_type):
        amount = self.input_amount(transaction_type)
        description = self.input_description()
        category = self.input_category()

        transaction = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': transaction_type,
            'amount': amount,
            'description': description,
            'category': category
        }

        transactions = self.load_transactions()
        transactions.append(transaction)
        self.save_transaction(transactions)
        print(f"{transaction_type.capitalize()} berhasil dicatat!")

    def view_transactions(self):
        transactions = self.load_transactions()
        if not transactions:
            print("Belum ada transaksi yang tercatat.")
            return

        headers = ["Tanggal", "Tipe", "Jumlah", "Kategori", "Deskripsi"]
        rows = []
        for t in transactions:
            rows.append([
                t['date'],
                t['type'],
                f"Rp{t['amount']:,.2f}",
                t['category'],
                t['description']
            ])

        display_table(headers, rows)

    def view_transactions_by_category(self):
        print("\nPilih kategori:")
        for num, cat in self.CATEGORIES.items():
            print(f"{num}. {cat}")

        category_choice = input("Pilih kategori: ").strip()
        selected_category = self.CATEGORIES.get(category_choice, None)

        if not selected_category:
            print("Kategori tidak valid.")
            return

        transactions = self.load_transactions()
        filtered = [t for t in transactions if t['category'] == selected_category]

        if not filtered:
            print(f"Tidak ada transaksi dalam kategori {selected_category}.")
            return

        headers = ["Tanggal", "Tipe", "Jumlah", "Deskripsi"]
        rows = []
        for t in filtered:
            rows.append([
                t['date'],
                t['type'],
                f"Rp{t['amount']:,.2f}",
                t['description']
            ])

        print(f"\nTransaksi dalam kategori {selected_category}:")
        display_table(headers, rows)

    def run(self):
        while True:
            print("\nPencatatan Transaksi Keuangan:")
            print("1. Pencatatan pemasukan")
            print("2. Pencatatan pengeluaran")
            print("3. Lihat semua transaksi")
            print("4. Lihat transaksi berdasarkan kategori")
            print("9. Kembali")

            choice = input("Pilih menu: ").strip()

            if choice == '1':
                self.record_transaction('pemasukan')
            elif choice == '2':
                self.record_transaction('pengeluaran')
            elif choice == '3':
                self.view_transactions()
            elif choice == '4':
                self.view_transactions_by_category()
            elif choice == '9':
                print("Keluar dari menu pencatatan transaksi.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")