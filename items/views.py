from django.http import HttpResponse

from homepage.views import page
from models.items import (
    CHEST_PARAMETER_ID, find_item_by_id, get_fit_status, is_item_suitable,
)
from models.parameters import get_parameter_by_id
from storage import load_items, load_parameters, load_users, load_values


def items(request):
    """Список вещей пользователей."""
    users_list = load_users("data/users.json")
    rows = ""
    for item in load_items("data/items.json", users_list):
        rows += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/items/{item.id}/">{item.name} ({item.user.name})</a>
            <span class="badge bg-secondary">размер {item.size}</span>
        </li>
        """
    content = f"""
    <h1>Вещи</h1>
    <ul class="list-group">{rows}</ul>
    """
    return HttpResponse(page("Вещи", content))


def item_detail(request, item_id):
    """Страница вещи с проверкой размера; если вещи нет – ответ 404."""
    users_list = load_users("data/users.json")
    parameters_list = load_parameters("data/parameters.json")
    item = find_item_by_id(load_items("data/items.json", users_list), item_id)
    if item is None:
        content = """
        <h1 class="text-danger">Вещь не найдена</h1>
        <a href="/items/" class="btn btn-outline-secondary">
            ← к списку вещей
        </a>
        """
        return HttpResponse(page("Вещь не найдена", content), status=404)
    values_list = load_values(
        "data/measurements.json", users_list, parameters_list)
    chest = get_parameter_by_id(parameters_list, CHEST_PARAMETER_ID)
    suitable = is_item_suitable(values_list, item, chest)
    badge = {True: "bg-success", False: "bg-danger", None: "bg-secondary"}
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{item.name}</h5>
            <p class="card-text"><strong>Владелец:</strong>
                {item.user.name}</p>
            <p class="card-text"><strong>Размер вещи:</strong> {item.size}</p>
            <p class="card-text">
                <span class="badge {badge[suitable]}">
                    {get_fit_status(suitable)}
                </span>
            </p>
            <a href="/items/" class="btn btn-outline-secondary">
                ← к списку вещей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(item.name, content), status=200)
