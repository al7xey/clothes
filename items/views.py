from django.http import Http404
from django.shortcuts import render

from models.items import (
    CHEST_PARAMETER_ID, find_item_by_id, get_fit_status, is_item_suitable,
)
from models.parameters import get_parameter_by_id
from storage import load_items, load_parameters, load_users, load_values


def items(request):
    """Список вещей пользователей."""
    users_list = load_users("data/users.json")
    context = {"items": load_items("data/items.json", users_list)}
    return render(request, "items/list.html", context)


def item_detail(request, item_id):
    """Страница вещи с проверкой размера; если вещи нет – ответ 404."""
    users_list = load_users("data/users.json")
    parameters_list = load_parameters("data/parameters.json")
    item = find_item_by_id(load_items("data/items.json", users_list), item_id)
    if item is None:
        raise Http404("Вещь не найдена")
    values_list = load_values(
        "data/measurements.json", users_list, parameters_list)
    chest = get_parameter_by_id(parameters_list, CHEST_PARAMETER_ID)
    suitable = is_item_suitable(values_list, item, chest)
    context = {
        "item": item,
        "suitable": suitable,
        "fit_status": get_fit_status(suitable),
    }
    return render(request, "items/detail.html", context)
