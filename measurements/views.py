from django.http import Http404
from django.shortcuts import render

from db.database import fetch_all, fetch_one


def measurements(request):
    """Список мерок пользователей (JOIN трёх таблиц)."""
    context = {"values": fetch_all("list_measurements")}
    return render(request, "measurements/list.html", context)


def measurement_detail(request, value_id):
    """Страница мерки; если мерки нет – ответ 404."""
    value = fetch_one("measurement_by_id", (value_id,))
    if value is None:
        raise Http404("Мерка не найдена")
    return render(request, "measurements/detail.html", {"value": value})


def measurements_by_date(request):
    """Поиск мерок по дате: параметр запроса ?date=ГГГГ-ММ-ДД."""
    date = request.GET.get("date", "").strip()
    found = fetch_all("measurements_by_date", (date,)) if date else None
    context = {
        "date": date,
        "values": found,
        "dates": fetch_all("measurement_dates"),
    }
    return render(request, "measurements/by_date.html", context)
