import math
from utils.api_utils import get_interest_rate
from modules.savings_strategy import SavingsStrategy, ConservativeStrategy

class SavingsCalculator:
    def _init_(self):
        self.strategy = ConservativeStrategy()  # default strategy

    def set_strategy(self, strategy: SavingsStrategy):
        self.strategy = strategy

    def calculate_with_strategy(self):
        income = float(input("Masukkan pendapatan bulanan: "))
        expenses = float(input("Masukkan pengeluaran bulanan: "))
        savings = self.strategy.calculate_savings(income, expenses)
        print(f"\nSisa tabungan bulanan berdasarkan strategi: Rp{savings:,.2f}")

    def calculate_savings_growth(self):
        principal = float(input("Masukkan jumlah tabungan awal: "))
        monthly_deposit = float(input("Masukkan setoran bulanan: "))
        years = int(input("Masukkan jangka waktu (tahun): "))
        interest_rate = get_interest_rate() / 100

        monthly_rate = interest_rate / 12
        months = years * 12

        future_value = principal * (1 + monthly_rate) ** months
        future_value += monthly_deposit * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)

        print(f"\nNilai tabungan setelah {years} tahun: Rp{future_value:,.2f}")

    def calculate_saving_time(self):
        target = float(input("Masukkan target tabungan: "))
        monthly_deposit = float(input("Masukkan setoran bulanan: "))
        interest_rate = get_interest_rate() / 100

        if monthly_deposit <= 0:
            print("Setoran bulanan harus lebih dari 0")
            return

        if interest_rate == 0:
            months = target / monthly_deposit
        else:
            monthly_rate = interest_rate / 12
            months = math.log(1 + (target * monthly_rate) / monthly_deposit) / math.log(1 + monthly_rate)

        years = months / 12
        print(f"\nWaktu yang dibutuhkan: {years:.1f} tahun")

    def run(self):
        while True:
            print("\nKalkulator Tabungan dan Simpanan:")
            print("1. Menghitung pertumbuhan tabungan berdasarkan jumlah setoran tetap")
            print("2. Menghitung waktu yang dibutuhkan untuk mencapai target tabungan")
            print("3. Menghitung sisa tabungan menggunakan strategi pengelolaan")
            print("9. Kembali")

            choice = input("Pilih menu: ")

            if choice == '1':
                self.calculate_savings_growth()
            elif choice == '2':
                self.calculate_saving_time()
            elif choice == '3':
                self.calculate_with_strategy()
            elif choice == '9':
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")