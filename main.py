"""ПР1. Начальный сценарий: подбор размера одежды по мерке."""
from datetime import date

PARAMETERS = {
    "chest": ("Обхват груди", "см"),
    "waist": ("Обхват талии", "см"),
    "hips": ("Обхват бёдер", "см"),
    "height": ("Рост", "см"),
}

user_name = "Алексей"
parameter_code = "chest"
measured_value = 98.5
measure_date = date(2026, 9, 15)
item_size = "L"


def get_parameter_info(code):
    """Вернуть название и единицу измерения параметра по коду."""
    if code in PARAMETERS:
        return PARAMETERS[code]
    return "Неизвестный параметр", ""


def is_value_valid(code, value):
    """Проверить, что значение мерки лежит в допустимых пределах."""
    if code == "height":
        return 50 <= value <= 250
    return 30 <= value <= 200


def recommend_size(chest):
    """Подобрать буквенный размер по обхвату груди (см)."""
    if chest < 88:
        return "XS"
    elif chest < 94:
        return "S"
    elif chest < 100:
        return "M"
    elif chest < 106:
        return "L"
    elif chest < 112:
        return "XL"
    return "XXL"


def is_item_suitable(recommended, size):
    """Проверить, совпадает ли размер вещи с рекомендованным."""
    return recommended == size


def build_report(name, code, value, measured_on, size):
    """Сформировать текстовый отчёт по одной мерке."""
    title, unit = get_parameter_info(code)
    if not is_value_valid(code, value):
        return f"Ошибка: значение {value} {unit} недопустимо"
    recommended = recommend_size(value)
    if is_item_suitable(recommended, size):
        verdict = "вещь подходит"
    else:
        verdict = "вещь не подходит"
    return (
        f"Пользователь: {name}\n"
        f"Дата измерения: {measured_on}\n"
        f"{title}: {value} {unit}\n"
        f"Рекомендуемый размер: {recommended}\n"
        f"Размер вещи: {size} — {verdict}"
    )


print(build_report(user_name, parameter_code, measured_value,
                   measure_date, item_size))
