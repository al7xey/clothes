from django.http import HttpResponse

from homepage.views import page
from models.values import find_value_by_id
from storage import load_parameters, load_users, load_values


def _load_all_values():
    """Загрузить мерки вместе со связанными пользователями и параметрами."""
    users_list = load_users("data/users.json")
    parameters_list = load_parameters("data/parameters.json")
    return load_values("data/measurements.json", users_list, parameters_list)


def measurements(request):
    """Список мерок пользователей."""
    items = ""
    for value in _load_all_values():
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/measurements/{value.id}/">
                {value.user.name}: {value.parameter.name}
            </a>
            <span class="badge bg-success">
                {value.amount} {value.parameter.unit}
            </span>
        </li>
        """
    content = f"""
    <h1>Мерки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Мерки", content))


def measurement_detail(request, value_id):
    """Страница мерки; если мерки нет – ответ 404."""
    value = find_value_by_id(_load_all_values(), value_id)
    if value is None:
        content = """
        <h1 class="text-danger">Мерка не найдена</h1>
        <a href="/measurements/" class="btn btn-outline-secondary">
            ← к списку мерок
        </a>
        """
        return HttpResponse(page("Мерка не найдена", content), status=404)
    badge = "bg-success" if value.is_in_range() else "bg-danger"
    status = "в допустимых пределах" if value.is_in_range() else "вне пределов"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Мерка №{value.id}</h5>
            <p class="card-text">Пользователь: {value.user.name}</p>
            <p class="card-text">Параметр: {value.parameter.name}</p>
            <p class="card-text">
                Значение: {value.amount} {value.parameter.unit}
            </p>
            <p class="card-text">Дата: {value.value_date}</p>
            <p class="card-text">
                Проверка: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/measurements/" class="btn btn-outline-secondary">
                ← к списку мерок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Мерка №{value.id}", content), status=200)
