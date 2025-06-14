import json
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

    def __init__(self):
        self.transactions_file = 'data/transactions.json'

    def load_transactions(self):
        try:
            with open(self.transactions_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_transaction(self, transactions):
        with open(self.transactions_file, 'w') as f:
            json.dump(transactions, f, indent=2)

    def record_transaction(self, transaction_type):
        amount = float(input(f"Masukkan jumlah {transaction_type}: "))
        description = input("Masukkan deskripsi: ")
        
        print("\nKategori:")
        for num, cat in self.CATEGORIES.items():
            print(f"{num}. {cat}")
        
        category_choice = input("Pilih kategori: ")
        category = self.CATEGORIES.get(category_choice, 'Lainnya')
        
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
        print(f"{transaction_type} berhasil dicatat!")

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

    def run(self):
        while True:
            print("\nPencatatan Transaksi Keuangan:")
            print("1. Pencatatan pemasukan")
            print("2. Pencatatan pengeluaran")
            print("3. Lihat semua transaksi")
            print("4. Lihat transaksi berdasarkan kategori")
            print("9. Kembali")
            
            choice = input("Pilih menu: ")
            
            if choice == '1':
                self.record_transaction('pemasukan')
            elif choice == '2':
                self.record_transaction('pengeluaran')
            elif choice == '3':
                self.view_transactions()
            elif choice == '4':
                self.view_transactions_by_category()
            elif choice == '9':
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    def view_transactions_by_category(self):
        print("\nPilih kategori:")
        for num, cat in self.CATEGORIES.items():
            print(f"{num}. {cat}")
        
        category_choice = input("Pilih kategori: ")
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