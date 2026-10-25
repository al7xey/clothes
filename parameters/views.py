from django.http import Http404
from django.shortcuts import render

from db.database import fetch_all, fetch_one


def parameters(request):
    """Список параметров из базы данных."""
    context = {"parameters": fetch_all("list_parameters")}
    return render(request, "parameters/list.html", context)


def parameter_detail(request, parameter_id):
    """Страница параметра; если параметра нет – ответ 404."""
    parameter = fetch_one("parameter_by_id", (parameter_id,))
    if parameter is None:
        raise Http404("Параметр не найден")
    return render(request, "parameters/detail.html", {"parameter": parameter})
