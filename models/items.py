"""Класс Item (вещь) и функции работы с коллекцией вещей."""
from typing import Any, List, Optional

from .base import Entity
from .parameters import Parameter
from .users import User
from .values import Value, get_latest_amount

SIZE_CHART = [
    ("XS", 88),
    ("S", 94),
    ("M", 100),
    ("L", 106),
    ("XL", 112),
]
CHEST_PARAMETER_ID = 1


class Item(Entity):
    """Вещь пользователя с указанным размером."""

    def __init__(self, item_id: int, user: User, name: str, size: str) -> None:
        """Создать вещь."""
        super().__init__(item_id)
        self.user = user
        self.name = name
        self.size = size.upper()

    @staticmethod
    def recommend_size(chest: float) -> str:
        """Подобрать буквенный размер по обхвату груди (см)."""
        for size, upper_bound in SIZE_CHART:
            if chest < upper_bound:
                return size
        return "XXL"

    def is_suitable_for(self, chest: float) -> bool:
        """Проверить, подходит ли размер вещи при данном обхвате груди."""
        return self.recommend_size(chest) == self.size

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать вещь в данные JSON: ссылка на User -> user_id."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "name": self.name,
            "size": self.size,
        }

    def __str__(self) -> str:
        """Строковое представление вещи."""
        return f"{self.name} ({self.size}), {self.user.name}"


def add_item(items: List[Item], user: User, name: str, size: str) -> Item:
    """Создать вещь и добавить её в коллекцию."""
    new_id = max((i.id for i in items), default=0) + 1
    item = Item(new_id, user, name, size)
    items.append(item)
    return item


def find_item(items: List[Item], query: str) -> List[Item]:
    """Найти вещи по подстроке названия."""
    query = query.lower()
    return [i for i in items if query in i.name.lower()]


def is_item_suitable(
    values: List[Value], item: Item, chest: Parameter
) -> Optional[bool]:
    """Проверить вещь по последней мерке груди владельца.

    Возвращает None, если у владельца нет мерки обхвата груди.
    """
    amount = get_latest_amount(values, item.user, chest)
    if amount is None:
        return None
    return item.is_suitable_for(amount)


def get_fit_status(is_suitable: Optional[bool]) -> str:
    """Текстовый статус вещи (функция из ПР1)."""
    if is_suitable is None:
        return "Нет мерки обхвата груди — проверить нельзя"
    if is_suitable:
        return "Вещь подходит по размеру"
    return "Вещь не подходит по размеру"


def show_items(items: List[Item]) -> None:
    """Вывести вещи."""
    for item in items:
        print(f"{item.id}. {item}")
