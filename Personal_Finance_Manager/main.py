import os
from modules.transaction_recorder import TransactionRecorder
from modules.budget_planner import BudgetPlanner
def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    for file in ['transactions.json', 'budgets.json', 'goals.json']:
        if not os.path.exists(f'data/{file}'):
            with open(f'data/{file}', 'w') as f:
                f.write('[]')

    while True:
        print("\nManajemen Keuangan Pribadi:")
        print("1. Pencatatan Transaksi Keuangan")
        print("2. Perencanaan dan Pemantauan Anggaran")
        print("3. Kalkulator Tabungan dan Simpanan")
        print("4. Ringkasan Keuangan Bulanan")
        print("5. Perencanaan Tujuan Keuangan")
        print("9. Keluar")

        choice = input("Pilih menu: ")

        if choice == '1':
            TransactionRecorder().run()
        elif choice == '2':
            BudgetPlanner().run()
        elif choice == '3':
            SavingsCalculator().run()
        elif choice == '4':
            MonthlySummary().run()
        elif choice == '5':
            FinancialGoals().run()
        elif choice == '9':
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
