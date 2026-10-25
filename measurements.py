"""Значения мерок пользователей."""
from datetime import date
from typing import Optional

from parameters import check_value_in_range


def is_measurement_exists(
    measurements: list[dict],
    user_id: int,
    parameter_id: int,
    measure_date: date,
) -> bool:
    """Проверить, есть ли уже мерка этого параметра на эту дату."""
    iso_date = measure_date.isoformat()
    for measurement in measurements:
        if (
            measurement["user_id"] == user_id
            and measurement["parameter_id"] == parameter_id
            and measurement["date"] == iso_date
        ):
            return True
    return False


def add_measurement(
    measurements: list[dict],
    parameters: dict[int, dict],
    user_id: int,
    parameter_id: int,
    value: float,
    measure_date: date,
) -> Optional[dict]:
    """Добавить мерку; вернуть её или None, если добавить нельзя.

    Нельзя добавить значение вне допустимых пределов и вторую мерку
    одного параметра у одного пользователя на одну и ту же дату.
    """
    if not check_value_in_range(parameters, parameter_id, value):
        return None
    if is_measurement_exists(
        measurements, user_id, parameter_id, measure_date
    ):
        return None
    new_id = max((m["id"] for m in measurements), default=0) + 1
    measurement = {
        "id": new_id,
        "user_id": user_id,
        "parameter_id": parameter_id,
        "value": value,
        "date": measure_date.isoformat(),
    }
    measurements.append(measurement)
    return measurement


def remove_measurement(measurements: list[dict], measurement_id: int) -> bool:
    """Удалить мерку по идентификатору; вернуть True при успехе."""
    for measurement in measurements:
        if measurement["id"] == measurement_id:
            measurements.remove(measurement)
            return True
    return False


def get_user_measurements(
    measurements: list[dict], user_id: int
) -> list[dict]:
    """Вернуть мерки пользователя, отсортированные по дате."""
    own = [m for m in measurements if m["user_id"] == user_id]
    return sorted(own, key=lambda m: m["date"])


def get_latest_value(
    measurements: list[dict], user_id: int, parameter_id: int
) -> Optional[float]:
    """Вернуть последнее значение параметра пользователя или None."""
    values = [
        m for m in get_user_measurements(measurements, user_id)
        if m["parameter_id"] == parameter_id
    ]
    if not values:
        return None
    return values[-1]["value"]
