from models import Entity, Parameter
from models.parameters import (
    add_parameter, check_value_in_range, filter_parameters_by_unit,
    find_parameter, sort_parameters,
)


def make_parameters():
    parameters = []
    add_parameter(parameters, "Обхват груди", "см", 60, 150)
    add_parameter(parameters, "Вес", "кг", 30, 200)
    return parameters


def test_parameter_creation_and_str():
    parameter = Parameter(1, "Рост", "см", 100, 230)
    assert isinstance(parameter, Entity)
    assert parameter.id == 1
    assert parameter.name == "Рост"
    assert str(parameter) == "Рост, см (допустимо 100–230)"


def test_is_value_valid_method():
    parameter = Parameter(1, "Рост", "см", 100, 230)
    assert parameter.is_value_valid(182)
    assert not parameter.is_value_valid(50)


def test_validate_range_staticmethod():
    assert Parameter.validate_range(50, 150)
    assert not Parameter.validate_range(150, 50)


def test_from_data_and_to_dict_roundtrip():
    data = {"id": 3, "name": "Талия", "unit": "см", "min": 50, "max": 150}
    assert Parameter.from_data(data).to_dict() == data


def test_add_parameter_returns_object_and_rejects_bad_range():
    parameters = []
    created = add_parameter(parameters, "Талия", "см", 50, 150)
    assert created is parameters[0]
    assert add_parameter(parameters, "Плохой", "см", 90, 10) is None
    assert len(parameters) == 1


def test_find_filter_sort_check():
    parameters = make_parameters()
    assert [p.id for p in find_parameter(parameters, "обхват")] == [1]
    assert len(filter_parameters_by_unit(parameters, "кг")) == 1
    names = [p.name for p in sort_parameters(parameters)]
    assert names == sorted(names)
    assert check_value_in_range(parameters, 1, 98.5)
    assert not check_value_in_range(parameters, 99, 50)
