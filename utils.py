"""Вспомогательные функции безопасного ввода."""
from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить целое число; при ошибке повторить запрос."""
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: нужно ввести целое число.")


def input_float(prompt: str) -> float:
    """Запросить число (допускается запятая); при ошибке повторить."""
    while True:
        raw = input(prompt).replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: нужно ввести число.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ; при ошибке повторить."""
    while True:
        raw = input(prompt)
        try:
            return datetime.strptime(raw, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: формат даты ДД.ММ.ГГГГ, например 15.09.2026.")
