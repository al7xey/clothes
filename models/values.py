"""Класс Value (значение мерки) и функции работы с коллекцией значений."""
from datetime import date
from typing import Any, List, Optional

from .base import Entity
from .parameters import Parameter
from .users import User


class Value(Entity):
    """Значение параметра, измеренное у пользователя.

    Хранит ссылки на объекты User и Parameter (композиция), а не только
    их идентификаторы.
    """

    def __init__(
        self,
        value_id: int,
        user: User,
        parameter: Parameter,
        amount: float,
        value_date: str,
    ) -> None:
        """Создать значение мерки."""
        super().__init__(value_id)
        self.user = user
        self.parameter = parameter
        self.amount = amount
        self.value_date = value_date

    def is_in_range(self) -> bool:
        """Проверить значение по пределам его параметра."""
        return self.parameter.is_value_valid(self.amount)

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать в данные JSON: ссылки заменяются на id."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "parameter_id": self.parameter.id,
            "value": self.amount,
            "date": self.value_date,
        }

    def __str__(self) -> str:
        """Строковое представление значения мерки."""
        return (f"{self.value_date}: {self.user.name}, "
                f"{self.parameter.name} = {self.amount} {self.parameter.unit}")


def is_value_exists(
    values: List[Value],
    user: User,
    parameter: Parameter,
    value_date: date,
) -> bool:
    """Проверить, есть ли уже значение этого параметра на эту дату."""
    iso_date = value_date.isoformat()
    for value in values:
        if (
            value.user.id == user.id
            and value.parameter.id == parameter.id
            and value.value_date == iso_date
        ):
            return True
    return False


def add_value(
    values: List[Value],
    user: User,
    parameter: Parameter,
    amount: float,
    value_date: date,
) -> Optional[Value]:
    """Создать значение мерки и добавить его в коллекцию.

    Возвращает None, если значение вне допустимых пределов или такая
    мерка на эту дату уже есть.
    """
    if not parameter.is_value_valid(amount):
        return None
    if is_value_exists(values, user, parameter, value_date):
        return None
    new_id = max((v.id for v in values), default=0) + 1
    value = Value(new_id, user, parameter, amount, value_date.isoformat())
    values.append(value)
    return value


def remove_value(values: List[Value], value_id: int) -> bool:
    """Удалить значение по идентификатору; True при успехе."""
    for value in values:
        if value.id == value_id:
            values.remove(value)
            return True
    return False


def get_user_values(values: List[Value], user: User) -> List[Value]:
    """Вернуть значения пользователя, отсортированные по дате."""
    own = [v for v in values if v.user.id == user.id]
    return sorted(own, key=lambda v: v.value_date)


def get_latest_amount(
    values: List[Value], user: User, parameter: Parameter
) -> Optional[float]:
    """Вернуть последнее значение параметра пользователя или None."""
    amounts = [
        v for v in get_user_values(values, user)
        if v.parameter.id == parameter.id
    ]
    if not amounts:
        return None
    return amounts[-1].amount


def show_values(values: List[Value], user: User) -> None:
    """Вывести значения пользователя."""
    own = get_user_values(values, user)
    if not own:
        print("У пользователя нет мерок")
    for value in own:
        print(f"#{value.id} {value}")


def find_value_by_id(
    values: List[Value], value_id: int
) -> Optional[Value]:
    """Найти значение мерки по идентификатору."""
    for value in values:
        if value.id == value_id:
            return value
    return None
