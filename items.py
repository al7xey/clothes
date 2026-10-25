"""Вещи и подбор размера."""
from typing import Optional

from measurements import get_latest_value

CHEST_PARAMETER_ID = 1
SIZE_CHART = [
    ("XS", 88),
    ("S", 94),
    ("M", 100),
    ("L", 106),
    ("XL", 112),
]


def recommend_size(chest: float) -> str:
    """Подобрать буквенный размер по обхвату груди (см)."""
    for size, upper_bound in SIZE_CHART:
        if chest < upper_bound:
            return size
    return "XXL"


def add_item(items: list[dict], user_id: int, name: str, size: str) -> dict:
    """Добавить вещь пользователя и вернуть её."""
    new_id = max((i["id"] for i in items), default=0) + 1
    item = {
        "id": new_id,
        "user_id": user_id,
        "name": name,
        "size": size.upper(),
    }
    items.append(item)
    return item


def find_item(items: list[dict], query: str) -> list[dict]:
    """Найти вещи по подстроке названия."""
    query = query.lower()
    return [i for i in items if query in i["name"].lower()]


def is_item_suitable(
    measurements: list[dict], user_id: int, size: str
) -> Optional[bool]:
    """Проверить, подходит ли размер вещи по последней мерке груди.

    Возвращает None, если у пользователя нет мерки обхвата груди.
    """
    chest = get_latest_value(measurements, user_id, CHEST_PARAMETER_ID)
    if chest is None:
        return None
    return recommend_size(chest) == size.upper()


def get_fit_status(is_suitable: Optional[bool]) -> str:
    """Текстовый статус вещи (развитие функции из ПР1)."""
    if is_suitable is None:
        return "Нет мерки обхвата груди — проверить нельзя"
    if is_suitable:
        return "Вещь подходит по размеру"
    return "Вещь не подходит по размеру"
