# API приложения

## Класс `FinanceCalculator`

### `add_operation(kind: str, amount: float, category: str) -> None`

Добавляет операцию и сохраняет её в `finance_data.json`.

- `kind` — `income` (доход) или `expense` (расход);
- `amount` — положительная сумма;
- `category` — категория операции.

### `show_operations() -> None`

Выводит нумерованный список операций с датой, знаком и суммой.

### `balance() -> float`

Возвращает разницу между доходами и расходами.

## Хранение данных

Файл `finance_data.json` содержит массив объектов:

```json
[
  {"kind": "income", "amount": 50000, "category": "Зарплата", "date": "2026-10-21"}
]
```
