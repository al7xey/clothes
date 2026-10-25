"""Загрузка и сохранение данных в JSON-файлах."""
import json
from typing import Any

DATA_DIR = "data"


def _read_json(filename: str) -> list[dict[str, Any]]:
    """Прочитать список записей из JSON-файла.

    Отсутствующий файл считается пустым хранилищем, а повреждённый
    JSON приводит к понятной ошибке ValueError.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(f"Файл {filename} повреждён: {error}") from error
    if not isinstance(data, list):
        raise ValueError(f"Файл {filename}: ожидается список записей")
    return data


def _write_json(filename: str, records: list[dict[str, Any]]) -> None:
    """Записать список записей в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_users(filename: str) -> dict[int, dict]:
    """Загрузить пользователей: словарь вида {id: данные}."""
    return {record["id"]: record for record in _read_json(filename)}


def save_users(filename: str, users: dict[int, dict]) -> None:
    """Сохранить пользователей в JSON-файл."""
    _write_json(filename, list(users.values()))


def load_parameters(filename: str) -> dict[int, dict]:
    """Загрузить параметры: словарь вида {id: данные}."""
    return {record["id"]: record for record in _read_json(filename)}


def save_parameters(filename: str, parameters: dict[int, dict]) -> None:
    """Сохранить параметры в JSON-файл."""
    _write_json(filename, list(parameters.values()))


def load_measurements(filename: str) -> list[dict]:
    """Загрузить значения мерок."""
    return _read_json(filename)


def save_measurements(filename: str, measurements: list[dict]) -> None:
    """Сохранить значения мерок."""
    _write_json(filename, measurements)


def load_items(filename: str) -> list[dict]:
    """Загрузить вещи."""
    return _read_json(filename)


def save_items(filename: str, items: list[dict]) -> None:
    """Сохранить вещи."""
    _write_json(filename, items)
