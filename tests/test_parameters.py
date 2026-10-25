from parameters import (
    add_parameter, check_value_in_range, filter_parameters_by_unit,
    find_parameter, sort_parameters,
)


def make_parameters():
    parameters = {}
    add_parameter(parameters, "Обхват груди", "см", 60, 150)
    add_parameter(parameters, "Вес", "кг", 30, 200)
    return parameters


def test_add_parameter_assigns_ids():
    parameters = make_parameters()
    assert list(parameters) == [1, 2]


def test_find_parameter_ignores_case():
    result = find_parameter(make_parameters(), "обхват")
    assert [p["id"] for p in result] == [1]


def test_check_value_in_range():
    parameters = make_parameters()
    assert check_value_in_range(parameters, 1, 98.5)
    assert not check_value_in_range(parameters, 1, 10)
    assert not check_value_in_range(parameters, 99, 50)


def test_filter_and_sort():
    parameters = make_parameters()
    assert len(filter_parameters_by_unit(parameters, "кг")) == 1
    names = [p["name"] for p in sort_parameters(parameters)]
    assert names == sorted(names)
