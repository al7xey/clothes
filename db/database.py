"""Работа с базой данных SQLite: подключение и выполнение запросов."""
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path(
    os.environ.get("CLOTHES_DB", BASE_DIR / "data" / "clothes.sqlite"))
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
QUERIES_PATH = BASE_DIR / "sql" / "queries.sql"


def get_connection(path: Optional[Path] = None) -> sqlite3.Connection:
    """Открыть соединение; строки результата доступны по имени столбца."""
    connection = sqlite3.connect(path or DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def load_queries(path: Path = QUERIES_PATH) -> Dict[str, str]:
    """Прочитать файл queries.sql и вернуть запросы по их именам."""
    text = path.read_text(encoding="utf-8")
    queries = {}
    for block in re.split(r"^-- name:\s*", text, flags=re.MULTILINE)[1:]:
        name, _, body = block.partition("\n")
        queries[name.strip()] = body.strip()
    return queries


QUERIES = load_queries()


def init_db(connection: sqlite3.Connection) -> None:
    """Создать таблицы по файлу schema.sql."""
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def fetch_all(name: str, params: tuple = ()) -> List[sqlite3.Row]:
    """Выполнить именованный запрос и вернуть все строки."""
    with get_connection() as connection:
        return connection.execute(QUERIES[name], params).fetchall()


def fetch_one(name: str, params: tuple = ()) -> Optional[sqlite3.Row]:
    """Выполнить именованный запрос и вернуть одну строку или None."""
    with get_connection() as connection:
        return connection.execute(QUERIES[name], params).fetchone()


def fetch_value(name: str, params: tuple = ()) -> Any:
    """Вернуть первое поле первой строки (или None)."""
    row = fetch_one(name, params)
    return None if row is None else row[0]
