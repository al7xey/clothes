from django.http import HttpResponse

from homepage.views import page
from models.parameters import get_parameter_by_id
from storage import load_parameters


def parameters(request):
    """Список параметров (мерок), загруженных из JSON."""
    items = ""
    for parameter in load_parameters("data/parameters.json"):
        text = (f"{parameter.name}, {parameter.unit} "
                f"(допустимо {parameter.min_value}–{parameter.max_value})")
        items += (
            f'<li class="list-group-item">'
            f'<a href="/parameters/{parameter.id}/">{text}</a></li>'
        )
    content = f"""
    <h1>Параметры</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Параметры", content))


def parameter_detail(request, parameter_id):
    """Страница параметра; если параметра нет – ответ 404."""
    parameters_list = load_parameters("data/parameters.json")
    parameter = get_parameter_by_id(parameters_list, parameter_id)
    if parameter is None:
        content = """
        <h1 class="text-danger">Параметр не найден</h1>
        <a href="/parameters/" class="btn btn-outline-secondary">
            ← к списку параметров
        </a>
        """
        return HttpResponse(page("Параметр не найден", content), status=404)
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{parameter.name}</h5>
            <p class="card-text"><strong>ID:</strong> {parameter.id}</p>
            <p class="card-text">
                <strong>Единица измерения:</strong> {parameter.unit}
            </p>
            <p class="card-text">
                <strong>Допустимые значения:</strong>
                {parameter.min_value}–{parameter.max_value} {parameter.unit}
            </p>
            <a href="/parameters/" class="btn btn-outline-secondary">
                ← к списку параметров
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(parameter.name, content), status=200)
