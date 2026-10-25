from django.http import Http404
from django.shortcuts import render

from models.values import find_value_by_id
from storage import load_parameters, load_users, load_values


def _load_all_values():
    """Загрузить мерки вместе со связанными пользователями и параметрами."""
    users_list = load_users("data/users.json")
    parameters_list = load_parameters("data/parameters.json")
    return load_values("data/measurements.json", users_list, parameters_list)


def measurements(request):
    """Список мерок пользователей."""
    context = {"values": _load_all_values()}
    return render(request, "measurements/list.html", context)


def measurement_detail(request, value_id):
    """Страница мерки; если мерки нет – ответ 404."""
    value = find_value_by_id(_load_all_values(), value_id)
    if value is None:
        raise Http404("Мерка не найдена")
    context = {"value": value, "in_range": value.is_in_range()}
    return render(request, "measurements/detail.html", context)
