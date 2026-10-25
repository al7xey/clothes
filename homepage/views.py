from django.shortcuts import render

from db.database import fetch_all, fetch_value


def index(request):
    """Главная страница."""
    return render(request, "homepage/index.html")


def statistics(request):
    """Статистика по базе данных (COUNT и GROUP BY)."""
    context = {
        "users_total": fetch_value("count_users"),
        "measurements_total": fetch_value("count_measurements"),
        "items_total": fetch_value("count_items"),
        "per_parameter": fetch_all("measurements_per_parameter"),
        "items_per_user": fetch_all("items_per_user"),
        "active_users": fetch_all("measurements_per_user", (2,)),
    }
    return render(request, "homepage/statistics.html", context)


def page_not_found(request, exception):
    """Собственная страница ошибки 404."""
    return render(request, "404.html", status=404)
