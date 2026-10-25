"""Параметры (мерки): обхват груди, талии, бёдер, рост и т.д."""
from typing import Optional


def add_parameter(
    parameters: dict[int, dict],
    name: str,
    unit: str,
    min_value: float,
    max_value: float,
) -> int:
    """Добавить параметр в словарь и вернуть его идентификатор."""
    new_id = max(parameters, default=0) + 1
    parameters[new_id] = {
        "id": new_id,
        "name": name,
        "unit": unit,
        "min": min_value,
        "max": max_value,
    }
    return new_id


def get_parameter_info(
    parameters: dict[int, dict], parameter_id: int
) -> Optional[dict]:
    """Вернуть данные параметра по идентификатору или None."""
    return parameters.get(parameter_id)


def find_parameter(parameters: dict[int, dict], query: str) -> list[dict]:
    """Найти параметры по подстроке названия (без учёта регистра)."""
    query = query.lower()
    return [p for p in parameters.values() if query in p["name"].lower()]


def check_value_in_range(
    parameters: dict[int, dict], parameter_id: int, value: float
) -> bool:
    """Проверить, что значение лежит в допустимых пределах параметра."""
    parameter = parameters.get(parameter_id)
    if parameter is None:
        return False
    return parameter["min"] <= value <= parameter["max"]


def filter_parameters_by_unit(
    parameters: dict[int, dict], unit: str
) -> list[dict]:
    """Отобрать параметры с заданной единицей измерения."""
    return list(p for p in parameters.values() if p["unit"] == unit)


def sort_parameters(parameters: dict[int, dict]) -> list[dict]:
    """Отсортировать параметры по названию."""
    return sorted(parameters.values(), key=lambda p: p["name"])
