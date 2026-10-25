from items import (
    add_item, find_item, get_fit_status, is_item_suitable, recommend_size,
)


def test_recommend_size_bounds():
    assert recommend_size(80) == "XS"
    assert recommend_size(98.5) == "M"
    assert recommend_size(130) == "XXL"


def test_add_and_find_item():
    items = []
    add_item(items, 1, "Куртка", "l")
    assert items[0]["size"] == "L"
    assert find_item(items, "курт")


def test_is_item_suitable():
    measurements = [{"id": 1, "user_id": 1, "parameter_id": 1,
                     "value": 98.5, "date": "2026-09-15"}]
    assert is_item_suitable(measurements, 1, "M") is True
    assert is_item_suitable(measurements, 1, "L") is False
    assert is_item_suitable(measurements, 2, "M") is None


def test_fit_status_texts():
    assert "подходит" in get_fit_status(True)
    assert "не подходит" in get_fit_status(False)
    assert "Нет мерки" in get_fit_status(None)
