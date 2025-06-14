import json
import math
from utils.api_utils import get_investment_options
from memory_profiler import profile

class FinancialGoals:
    @profile
    def __init__(self):
        self.goals_file = 'data/goals.json'

    def load_goals(self):
        try:
            with open(self.goals_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_goals(self, goals):
        with open(self.goals_file, 'w') as f:
            json.dump(goals, f, indent=2)

    def create_goal(self):
        name = input("Masukkan nama tujuan keuangan: ")
        target_amount = float(input("Masukkan target jumlah: "))
        time_frame = int(input("Masukkan jangka waktu (tahun): "))
        
        goal = {
            'name': name,
            'target_amount': target_amount,
            'time_frame': time_frame,
            'current_amount': 0
        }

        goals = self.load_goals()
        goals.append(goal)
        self.save_goals(goals)
        print("Tujuan keuangan berhasil dibuat!")

    def view_goals(self):
        goals = self.load_goals()
        if not goals:
            print("Belum ada tujuan keuangan yang dibuat.")
            return

        print("\nDaftar Tujuan Keuangan:")
        for i, goal in enumerate(goals, 1):
            print(f"{i}. {goal['name']} - Target: Rp{goal['target_amount']:,.2f} dalam {goal['time_frame']} tahun")
            print(f"   Progress: Rp{goal['current_amount']:,.2f} dari Rp{goal['target_amount']:,.2f} ({goal['current_amount']/goal['target_amount']*100:.1f}%)")

    def recommend_strategy(self):
        goals = self.load_goals()
        if not goals:
            print("Belum ada tujuan keuangan yang dibuat.")
            return

        print("\nPilih tujuan untuk rekomendasi strategi:")
        for i, goal in enumerate(goals, 1):
            print(f"{i}. {goal['name']}")
        
        choice = int(input("Pilih nomor tujuan: ")) - 1
        
        if choice < 0 or choice >= len(goals):
            print("Pilihan tidak valid.")
            return
        
        goal = goals[choice]
        yearly_saving = goal['target_amount'] / goal['time_frame']
        monthly_saving = yearly_saving / 12
        
        print(f"\nUntuk mencapai {goal['name']} (Rp{goal['target_amount']:,.2f} dalam {goal['time_frame']} tahun):")
        print(f"- Anda perlu menabung Rp{yearly_saving:,.2f} per tahun")
        print(f"- Atau Rp{monthly_saving:,.2f} per bulan")

        options = get_investment_options()
        if options:
            print("\nRekomendasi Investasi:")
            for opt in options:
                print(f"- {opt['name']}: Perkiraan return {opt['return']}% per tahun")
                required = goal['target_amount'] / ((1 + opt['return']/100) ** goal['time_frame'])
                print(f"  Dengan investasi ini, Anda hanya perlu menabung Rp{required:,.2f} sekarang")
                print(f"  Atau Rp{required / goal['time_frame'] / 12:,.2f} per bulan")

    def run(self):
        while True:
            print("\nPerencanaan Tujuan Keuangan:")
            print("1. Penetapan tujuan keuangan")
            print("2. Rekomendasi strategi untuk mencapai tujuan lebih cepat")
            print("9. Kembali")
            
            choice = input("Pilih menu: ")
            
            if choice == '1':
                self.create_goal()
            elif choice == '2':
                self.view_goals()
                self.recommend_strategy()
            elif choice == '9':
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                
if __name__ == "__main__":
    calculator = FinancialGoalsCalculator()
    calculator.calculate_goal_time()