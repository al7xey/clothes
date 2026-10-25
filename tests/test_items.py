from datetime import date

from models import Item, Parameter, User
from models.items import (
    add_item, find_item, get_fit_status, is_item_suitable,
)
from models.values import add_value


def make_objects():
    user = User(1, "Алексей", "a@example.com")
    chest = Parameter(1, "Обхват груди", "см", 60, 150)
    return user, chest


def test_recommend_size_staticmethod():
    assert Item.recommend_size(80) == "XS"
    assert Item.recommend_size(98.5) == "M"
    assert Item.recommend_size(130) == "XXL"


def test_item_creation_str_and_suitability():
    user, _ = make_objects()
    item = Item(1, user, "Куртка", "l")
    assert item.size == "L"
    assert str(item) == "Куртка (L), Алексей"
    assert item.is_suitable_for(103)
    assert not item.is_suitable_for(90)


def test_add_and_find_item():
    user, _ = make_objects()
    items = []
    add_item(items, user, "Куртка", "L")
    assert find_item(items, "курт") == items


def test_is_item_suitable_uses_latest_value():
    user, chest = make_objects()
    values = []
    item = Item(1, user, "Рубашка", "M")
    assert is_item_suitable(values, item, chest) is None
    add_value(values, user, chest, 98.5, date(2026, 9, 15))
    assert is_item_suitable(values, item, chest) is True
    assert is_item_suitable(
        values, Item(2, user, "Куртка", "L"), chest) is False


def test_fit_status_texts():
    assert "не подходит" in get_fit_status(False)
    assert "подходит" in get_fit_status(True)
    assert "Нет мерки" in get_fit_status(None)
