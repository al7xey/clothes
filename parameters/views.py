from django.http import Http404
from django.shortcuts import render

from models.parameters import get_parameter_by_id
from storage import load_parameters


def parameters(request):
    """Список параметров (мерок), загруженных из JSON."""
    context = {"parameters": load_parameters("data/parameters.json")}
    return render(request, "parameters/list.html", context)


def parameter_detail(request, parameter_id):
    """Страница параметра; если параметра нет – ответ 404."""
    parameters_list = load_parameters("data/parameters.json")
    parameter = get_parameter_by_id(parameters_list, parameter_id)
    if parameter is None:
        raise Http404("Параметр не найден")
    return render(request, "parameters/detail.html", {"parameter": parameter})
