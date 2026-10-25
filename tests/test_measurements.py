from datetime import date

from measurements import (
    add_measurement, get_latest_value, is_measurement_exists,
    remove_measurement,
)
from parameters import add_parameter


def make_parameters():
    parameters = {}
    add_parameter(parameters, "Обхват груди", "см", 60, 150)
    return parameters


def test_is_measurement_exists_empty():
    assert not is_measurement_exists([], 1, 1, date(2026, 9, 15))


def test_duplicate_measurement_forbidden():
    measurements = []
    parameters = make_parameters()
    first = add_measurement(
        measurements, parameters, 1, 1, 98.5, date(2026, 9, 15))
    second = add_measurement(
        measurements, parameters, 1, 1, 99.0, date(2026, 9, 15))
    assert first is not None
    assert second is None
    assert len(measurements) == 1


def test_out_of_range_value_rejected():
    measurements = []
    result = add_measurement(
        measurements, make_parameters(), 1, 1, 500, date(2026, 9, 15))
    assert result is None


def test_latest_value_and_remove():
    measurements = []
    parameters = make_parameters()
    add_measurement(measurements, parameters, 1, 1, 96, date(2026, 8, 1))
    add_measurement(measurements, parameters, 1, 1, 98, date(2026, 9, 1))
    assert get_latest_value(measurements, 1, 1) == 98
    assert remove_measurement(measurements, 2)
    assert get_latest_value(measurements, 1, 1) == 96
    assert not remove_measurement(measurements, 42)
