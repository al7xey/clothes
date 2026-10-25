from datetime import date

from models import Parameter, User, Value
from models.values import (
    add_value, get_latest_amount, is_value_exists, remove_value,
)


def make_objects():
    user = User(1, "Алексей", "a@example.com")
    chest = Parameter(1, "Обхват груди", "см", 60, 150)
    return user, chest


def test_value_links_objects():
    user, chest = make_objects()
    value = Value(1, user, chest, 98.5, "2026-09-15")
    assert value.user is user
    assert value.parameter is chest
    assert value.is_in_range()
    assert "Обхват груди = 98.5 см" in str(value)


def test_to_dict_stores_identifiers_only():
    user, chest = make_objects()
    data = Value(1, user, chest, 98.5, "2026-09-15").to_dict()
    assert data == {"id": 1, "user_id": 1, "parameter_id": 1,
                    "value": 98.5, "date": "2026-09-15"}


def test_duplicate_value_forbidden():
    user, chest = make_objects()
    values = []
    first = add_value(values, user, chest, 98.5, date(2026, 9, 15))
    second = add_value(values, user, chest, 99.0, date(2026, 9, 15))
    assert first is not None
    assert second is None
    assert len(values) == 1
    assert is_value_exists(values, user, chest, date(2026, 9, 15))


def test_out_of_range_value_rejected():
    user, chest = make_objects()
    assert add_value([], user, chest, 500, date(2026, 9, 15)) is None


def test_latest_amount_and_remove():
    user, chest = make_objects()
    values = []
    add_value(values, user, chest, 96, date(2026, 8, 1))
    add_value(values, user, chest, 98, date(2026, 9, 1))
    assert get_latest_amount(values, user, chest) == 98
    assert remove_value(values, 2)
    assert get_latest_amount(values, user, chest) == 96
    assert not remove_value(values, 42)
