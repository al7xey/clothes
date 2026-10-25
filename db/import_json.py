"""Импорт данных из JSON-файлов в базу SQLite.

Запуск из корня проекта: python -m db.import_json
"""
import json
from pathlib import Path
from typing import List

from db.database import BASE_DIR, DB_PATH, get_connection, init_db

DATA_DIR = BASE_DIR / "data"


def _read(name: str) -> List[dict]:
    """Прочитать JSON-файл из каталога data."""
    with open(DATA_DIR / name, encoding="utf-8") as file:
        return json.load(file)


def import_all(path: Path = DB_PATH) -> None:
    """Пересоздать таблицы и загрузить в них данные из JSON."""
    with get_connection(path) as connection:
        init_db(connection)
        connection.executemany(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
            [(u["id"], u["name"], u["email"]) for u in _read("users.json")],
        )
        connection.executemany(
            "INSERT INTO parameters (id, name, unit, min_value, max_value) "
            "VALUES (?, ?, ?, ?, ?)",
            [(p["id"], p["name"], p["unit"], p["min"], p["max"])
             for p in _read("parameters.json")],
        )
        connection.executemany(
            "INSERT INTO measurements "
            "(id, user_id, parameter_id, amount, value_date) "
            "VALUES (?, ?, ?, ?, ?)",
            [(m["id"], m["user_id"], m["parameter_id"], m["value"], m["date"])
             for m in _read("measurements.json")],
        )
        connection.executemany(
            "INSERT INTO items (id, user_id, name, size) VALUES (?, ?, ?, ?)",
            [(i["id"], i["user_id"], i["name"], i["size"])
             for i in _read("items.json")],
        )
    print(f"Данные импортированы в {path}")


if __name__ == "__main__":
    import_all()
