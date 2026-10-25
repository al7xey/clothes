import pytest

from storage import load_measurements, load_users, save_users


def test_missing_file_gives_empty_data(tmp_path):
    assert load_measurements(str(tmp_path / "none.json")) == []


def test_save_and_load_users_roundtrip(tmp_path):
    filename = str(tmp_path / "users.json")
    users = {1: {"id": 1, "name": "Алексей", "email": "a@example.com"}}
    save_users(filename, users)
    assert load_users(filename) == users


def test_broken_json_raises_value_error(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text("{не json", encoding="utf-8")
    with pytest.raises(ValueError):
        load_users(str(broken))
