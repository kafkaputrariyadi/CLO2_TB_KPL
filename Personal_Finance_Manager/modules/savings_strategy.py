from abc import ABC, abstractmethod

class SavingsStrategy(ABC):
    @abstractmethod
    def calculate_savings(self, income: float, expenses: float) -> float:
        pass

class ConservativeStrategy(SavingsStrategy):
    def calculate_savings(self, income, expenses):
        return max((income - expenses) * 0.2, 0)

class AggressiveStrategy(SavingsStrategy):
    def calculate_savings(self, income, expenses):
        return max((income - expenses) * 0.5, 0)

class BalancedStrategy(SavingsStrategy):
    def calculate_savings(self, income, expenses):
        return max((income - expenses) * 0.35, 0)