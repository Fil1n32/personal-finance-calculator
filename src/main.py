"""Калькулятор личных финансов (MVP)."""

import csv
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

DATA_FILE = Path("finance_data.json")


@dataclass
class Operation:
    """Одна финансовая операция."""

    kind: str
    amount: float
    category: str
    date: str


class FinanceCalculator:
    """Учёт доходов и расходов."""

    def __init__(self) -> None:
        self.operations: list[Operation] = []
        self.load()

    def add_operation(self, kind: str, amount: float, category: str) -> None:
        """Добавляет доход или расход."""
        if kind not in ("income", "expense"):
            raise ValueError("Вид операции должен быть income или expense")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.operations.append(Operation(kind, amount, category, date.today().isoformat()))
        self.save()

    def show_operations(self) -> None:
        """Выводит список операций."""
        if not self.operations:
            print("Операций пока нет.")
            return
        for index, item in enumerate(self.operations, start=1):
            sign = "+" if item.kind == "income" else "-"
            print(f"{index}. {item.date} {sign}{item.amount:.2f} — {item.category}")

    def balance(self) -> float:
        """Возвращает текущий баланс."""
        income = sum(item.amount for item in self.operations if item.kind == "income")
        expense = sum(item.amount for item in self.operations if item.kind == "expense")
        return income - expense

    def save(self) -> None:
        """Сохраняет операции в JSON."""
        DATA_FILE.write_text(
            json.dumps([asdict(item) for item in self.operations], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def export_csv(self, filename: str = "operations.csv") -> None:
        """Экспортирует операции в CSV-файл."""
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Дата", "Вид", "Сумма", "Категория"])
            for item in self.operations:
                writer.writerow([item.date, item.kind, item.amount, item.category])

    def load(self) -> None:
        """Загружает операции из JSON."""
        if not DATA_FILE.exists():
            return
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        self.operations = [Operation(**item) for item in raw]


def read_amount(prompt: str) -> float:
    """Запрашивает сумму с проверкой."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Ошибка: введите положительное число.")


def main() -> None:
    """Интерактивное меню приложения."""
    calculator = FinanceCalculator()
    menu = (
        "\n1. Добавить доход\n"
        "2. Добавить расход\n"
        "3. Показать операции\n"
        "4. Показать баланс\n"
        "5. Экспорт операций в CSV\n"
        "0. Выход\n"
    )
    while True:
        print(menu)
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            calculator.add_operation("income", read_amount("Сумма дохода: "), input("Категория: "))
        elif choice == "2":
            calculator.add_operation("expense", read_amount("Сумма расхода: "), input("Категория: "))
        elif choice == "3":
            calculator.show_operations()
        elif choice == "4":
            print(f"Текущий баланс: {calculator.balance():.2f} руб.")
        elif choice == "5":
            calculator.export_csv()
            print("Операции экспортированы в operations.csv")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
