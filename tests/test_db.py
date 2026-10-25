"""Тесты работы с SQLite и SQL-запросами (ПР7)."""
import sqlite3

import pytest

from db.database import QUERIES, fetch_all, fetch_one, fetch_value
from db.database import get_connection, load_queries
from db.import_json import import_all


@pytest.fixture
def connection(tmp_path):
    """Временная база, заполненная из JSON."""
    path = tmp_path / "test.sqlite"
    import_all(path)
    with get_connection(path) as conn:
        yield conn


def test_import_fills_tables(connection):
    counts = {}
    for table in ("users", "parameters", "measurements", "items"):
        query = f"SELECT COUNT(*) FROM {table}"
        counts[table] = connection.execute(query).fetchone()[0]
    assert counts == {"users": 2, "parameters": 4,
                      "measurements": 3, "items": 2}


def test_rows_accessible_by_column_name(connection):
    row = connection.execute(QUERIES["list_users"]).fetchone()
    assert isinstance(row, sqlite3.Row)
    assert row["name"] == "Алексей Семенов"


def test_foreign_keys_enforced(connection):
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO items (user_id, name, size) VALUES (99, 'x', 'M')")


def test_queries_file_has_required_kinds():
    queries = load_queries()
    assert len(queries) >= 10
    text = "\n".join(queries.values()).upper()
    assert text.count("JOIN") >= 2
    assert text.count("WHERE") >= 2
    assert text.count("COUNT(") >= 2
    assert text.count("GROUP BY") >= 2


def test_list_parameters():
    assert len(fetch_all("list_parameters")) == 4


def test_parameter_by_id_and_missing():
    assert fetch_one("parameter_by_id", (1,))["name"] == "Обхват груди"
    assert fetch_one("parameter_by_id", (999,)) is None


def test_measurements_join():
    row = fetch_one("measurement_by_id", (1,))
    assert row["user_name"] == "Алексей Семенов"
    assert row["parameter_name"] == "Обхват груди"
    assert row["in_range"] == 1


def test_measurements_by_date():
    assert len(fetch_all("measurements_by_date", ("2026-09-15",))) == 2
    assert fetch_all("measurements_by_date", ("2000-01-01",)) == []


def test_counts():
    assert fetch_value("count_users") == 2
    assert fetch_value("count_measurements") == 3
    assert fetch_value("count_items") == 2


def test_group_by_queries():
    per_parameter = fetch_all("measurements_per_parameter")
    assert {r["parameter_name"]: r["total"] for r in per_parameter}[
        "Обхват груди"] == 2
    items = {r["user_name"]: r["total"] for r in fetch_all("items_per_user")}
    assert items == {"Алексей Семенов": 1, "Мария Иванова": 1}


def test_having_filters_groups():
    rows = fetch_all("measurements_per_user", (2,))
    assert [r["user_name"] for r in rows] == ["Алексей Семенов"]


def test_latest_amount():
    assert fetch_value("latest_amount", (1, 1)) == 98.5
    assert fetch_value("latest_amount", (2, 4)) is None
