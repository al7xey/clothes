"""Класс Parameter и функции работы с коллекцией параметров."""
from typing import Any, List, Optional

from .base import Entity


class Parameter(Entity):
    """Параметр (мерка): обхват груди, талии, бёдер, рост."""

    def __init__(
        self,
        parameter_id: int,
        name: str,
        unit: str,
        min_value: float,
        max_value: float,
    ) -> None:
        """Создать параметр с допустимым диапазоном значений."""
        super().__init__(parameter_id)
        self.name = name
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value

    def is_value_valid(self, amount: float) -> bool:
        """Проверить, что значение лежит в допустимых пределах."""
        return self.min_value <= amount <= self.max_value

    @staticmethod
    def validate_range(min_value: float, max_value: float) -> bool:
        """Проверить корректность диапазона (минимум меньше максимума)."""
        return 0 < min_value < max_value

    @classmethod
    def from_data(cls, data: dict) -> "Parameter":
        """Создать параметр из словаря данных JSON."""
        return cls(
            parameter_id=data["id"],
            name=data["name"],
            unit=data["unit"],
            min_value=data["min"],
            max_value=data["max"],
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать параметр в данные для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "min": self.min_value,
            "max": self.max_value,
        }

    def __str__(self) -> str:
        """Строковое представление параметра."""
        return (f"{self.name}, {self.unit} "
                f"(допустимо {self.min_value}–{self.max_value})")


def add_parameter(
    parameters: List[Parameter],
    name: str,
    unit: str,
    min_value: float,
    max_value: float,
) -> Optional[Parameter]:
    """Создать параметр и добавить его в коллекцию.

    Возвращает None, если диапазон некорректен.
    """
    if not Parameter.validate_range(min_value, max_value):
        return None
    new_id = max((p.id for p in parameters), default=0) + 1
    parameter = Parameter(new_id, name, unit, min_value, max_value)
    parameters.append(parameter)
    return parameter


def get_parameter_by_id(
    parameters: List[Parameter], parameter_id: int
) -> Optional[Parameter]:
    """Найти параметр по идентификатору."""
    for parameter in parameters:
        if parameter.id == parameter_id:
            return parameter
    return None


def find_parameter(parameters: List[Parameter], query: str) -> List[Parameter]:
    """Найти параметры по подстроке названия (без учёта регистра)."""
    query = query.lower()
    return [p for p in parameters if query in p.name.lower()]


def check_value_in_range(
    parameters: List[Parameter], parameter_id: int, amount: float
) -> bool:
    """Найти параметр и проверить значение методом объекта."""
    parameter = get_parameter_by_id(parameters, parameter_id)
    if parameter is None:
        return False
    return parameter.is_value_valid(amount)


def filter_parameters_by_unit(
    parameters: List[Parameter], unit: str
) -> List[Parameter]:
    """Отобрать параметры с заданной единицей измерения."""
    return list(p for p in parameters if p.unit == unit)


def sort_parameters(parameters: List[Parameter]) -> List[Parameter]:
    """Отсортировать параметры по названию."""
    return sorted(parameters, key=lambda p: p.name)


def show_parameters(parameters: List[Parameter]) -> None:
    """Вывести параметры."""
    for parameter in sort_parameters(parameters):
        print(f"{parameter.id}. {parameter}")
