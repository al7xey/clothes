import pytest

from models import Item, Parameter, User, Value
from storage import (
    load_items, load_users, load_values, save_items, save_users,
    save_values,
)


def make_objects():
    user = User(1, "Алексей", "a@example.com")
    chest = Parameter(1, "Обхват груди", "см", 60, 150)
    return user, chest


def test_missing_file_gives_empty_list(tmp_path):
    assert load_users(str(tmp_path / "none.json")) == []


def test_users_roundtrip_creates_objects(tmp_path):
    filename = str(tmp_path / "users.json")
    save_users(filename, [User(1, "Алексей", "a@example.com")])
    loaded = load_users(filename)
    assert isinstance(loaded[0], User)
    assert loaded[0].name == "Алексей"


def test_values_restore_links(tmp_path):
    user, chest = make_objects()
    filename = str(tmp_path / "values.json")
    save_values(filename, [Value(1, user, chest, 98.5, "2026-09-15")])
    loaded = load_values(filename, [user], [chest])
    assert loaded[0].user is user
    assert loaded[0].parameter is chest
    assert loaded[0].amount == 98.5


def test_value_with_unknown_user_raises(tmp_path):
    user, chest = make_objects()
    filename = str(tmp_path / "values.json")
    save_values(filename, [Value(1, user, chest, 98.5, "2026-09-15")])
    with pytest.raises(ValueError):
        load_values(filename, [], [chest])


def test_items_roundtrip(tmp_path):
    user, _ = make_objects()
    filename = str(tmp_path / "items.json")
    save_items(filename, [Item(1, user, "Куртка", "L")])
    loaded = load_items(filename, [user])
    assert loaded[0].user is user
    assert loaded[0].size == "L"


def test_broken_json_raises_value_error(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text("{не json", encoding="utf-8")
    with pytest.raises(ValueError):
        load_users(str(broken))
