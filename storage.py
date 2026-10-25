"""Преобразование между JSON-данными и объектами моделей."""
import json
from typing import Any, List

from models import Item, Parameter, User, Value
from models.parameters import get_parameter_by_id
from models.users import get_user_by_id

DATA_DIR = "data"


def _read_json(filename: str) -> List[dict[str, Any]]:
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


def _write_json(filename: str, records: List[dict[str, Any]]) -> None:
    """Записать список записей в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_users(filename: str) -> List[User]:
    """Загрузить пользователей как список объектов User."""
    return [User.from_data(record) for record in _read_json(filename)]


def save_users(filename: str, users: List[User]) -> None:
    """Сохранить объекты User в JSON-файл."""
    _write_json(filename, [user.to_dict() for user in users])


def load_parameters(filename: str) -> List[Parameter]:
    """Загрузить параметры как список объектов Parameter."""
    return [Parameter.from_data(record) for record in _read_json(filename)]


def save_parameters(filename: str, parameters: List[Parameter]) -> None:
    """Сохранить объекты Parameter в JSON-файл."""
    _write_json(filename, [p.to_dict() for p in parameters])


def load_values(
    filename: str, users: List[User], parameters: List[Parameter]
) -> List[Value]:
    """Загрузить значения мерок, восстановив ссылки на User и Parameter.

    Если пользователь или параметр не найден, данные считаются
    некорректными и возникает ValueError.
    """
    values = []
    for record in _read_json(filename):
        user = get_user_by_id(users, record["user_id"])
        parameter = get_parameter_by_id(parameters, record["parameter_id"])
        if user is None or parameter is None:
            raise ValueError(
                f"Значение #{record['id']}: пользователь или параметр "
                "не найден"
            )
        values.append(Value(
            record["id"], user, parameter, record["value"], record["date"]
        ))
    return values


def save_values(filename: str, values: List[Value]) -> None:
    """Сохранить значения; объекты-ссылки превращаются в идентификаторы."""
    _write_json(filename, [v.to_dict() for v in values])


def load_items(filename: str, users: List[User]) -> List[Item]:
    """Загрузить вещи, восстановив ссылку на владельца."""
    items = []
    for record in _read_json(filename):
        user = get_user_by_id(users, record["user_id"])
        if user is None:
            raise ValueError(f"Вещь #{record['id']}: владелец не найден")
        items.append(Item(record["id"], user, record["name"], record["size"]))
    return items


def save_items(filename: str, items: List[Item]) -> None:
    """Сохранить вещи в JSON-файл."""
    _write_json(filename, [item.to_dict() for item in items])
