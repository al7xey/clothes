from django.http import Http404
from django.shortcuts import render

from db.database import fetch_all, fetch_one, fetch_value
from models.items import CHEST_PARAMETER_ID, Item, get_fit_status


def items(request):
    """Список вещей пользователей (JOIN с владельцами)."""
    context = {"items": fetch_all("list_items")}
    return render(request, "items/list.html", context)


def item_detail(request, item_id):
    """Страница вещи с проверкой размера; если вещи нет – ответ 404."""
    item = fetch_one("item_by_id", (item_id,))
    if item is None:
        raise Http404("Вещь не найдена")
    chest = fetch_value("latest_amount", (item["user_id"], CHEST_PARAMETER_ID))
    suitable = None
    if chest is not None:
        suitable = Item.recommend_size(chest) == item["size"].upper()
    context = {
        "item": item,
        "suitable": suitable,
        "fit_status": get_fit_status(suitable),
    }
    return render(request, "items/detail.html", context)
