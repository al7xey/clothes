"""Система учета размеров одежды — консольное приложение (ПР2)."""
from datetime import date

from items import (
    add_item, find_item, get_fit_status, is_item_suitable, recommend_size,
    CHEST_PARAMETER_ID,
)
from measurements import (
    add_measurement, get_latest_value, get_user_measurements,
    remove_measurement,
)
from parameters import find_parameter, get_parameter_info, sort_parameters
from storage import (
    DATA_DIR, load_items, load_measurements, load_parameters, load_users,
    save_items, save_measurements,
)
from users import get_user
from utils import input_date, input_float, input_int

MENU = """
=== Система учета размеров одежды ===
1. Показать пользователей
2. Показать параметры
3. Найти параметр по названию
4. Добавить мерку
5. Показать мерки пользователя
6. Подобрать размер (отчёт)
7. Добавить вещь
8. Проверить, подходит ли вещь
9. Удалить мерку
0. Выход"""


def show_users(users: dict[int, dict]) -> None:
    """Вывести список пользователей."""
    for user in users.values():
        print(f"{user['id']}. {user['name']} <{user['email']}>")


def show_parameters(parameters: dict[int, dict]) -> None:
    """Вывести параметры, отсортированные по названию."""
    for p in sort_parameters(parameters):
        print(f"{p['id']}. {p['name']}, {p['unit']} "
              f"(допустимо {p['min']}–{p['max']})")


def show_measurements(
    measurements: list[dict], parameters: dict[int, dict], user_id: int
) -> None:
    """Вывести мерки пользователя."""
    own = get_user_measurements(measurements, user_id)
    if not own:
        print("У пользователя нет мерок")
    for m in own:
        p = parameters[m["parameter_id"]]
        print(f"#{m['id']} {m['date']}: {p['name']} = "
              f"{m['value']} {p['unit']}")


def build_report(
    users: dict[int, dict],
    parameters: dict[int, dict],
    measurements: list[dict],
    user_id: int,
    measure_date: date,
) -> str:
    """Отчёт по обхвату груди пользователя (функция из ПР1)."""
    user = get_user(users, user_id)
    chest = get_latest_value(measurements, user_id, CHEST_PARAMETER_ID)
    if user is None or chest is None:
        return "Недостаточно данных для отчёта"
    info = get_parameter_info(parameters, CHEST_PARAMETER_ID)
    return (
        f"Пользователь: {user['name']}\n"
        f"Дата отчёта: {measure_date}\n"
        f"{info['name']}: {chest} {info['unit']}\n"
        f"Рекомендуемый размер: {recommend_size(chest)}"
    )


def add_new_measurement(
    users: dict[int, dict],
    parameters: dict[int, dict],
    measurements: list[dict],
) -> None:
    """Сценарий добавления мерки."""
    user_id = input_int("ID пользователя: ")
    if get_user(users, user_id) is None:
        print("Пользователь не найден")
        return
    parameter_id = input_int("ID параметра: ")
    if get_parameter_info(parameters, parameter_id) is None:
        print("Параметр не найден")
        return
    value = input_float("Значение: ")
    measure_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    result = add_measurement(
        measurements, parameters, user_id, parameter_id, value, measure_date
    )
    if result is None:
        print("Мерка не добавлена: значение вне допустимых пределов "
              "или мерка на эту дату уже есть")
    else:
        print(f"Мерка добавлена, id={result['id']}")


def main() -> None:
    """Точка запуска: загрузка данных и цикл меню."""
    try:
        users = load_users(f"{DATA_DIR}/users.json")
        parameters = load_parameters(f"{DATA_DIR}/parameters.json")
        measurements = load_measurements(f"{DATA_DIR}/measurements.json")
        items = load_items(f"{DATA_DIR}/items.json")
    except ValueError as error:
        print(f"Не удалось загрузить данные: {error}")
        return
    try:
        run_menu(users, parameters, measurements, items)
    except (EOFError, KeyboardInterrupt):
        print("\nВвод прерван")
    save_measurements(f"{DATA_DIR}/measurements.json", measurements)
    save_items(f"{DATA_DIR}/items.json", items)
    print("Данные сохранены. До свидания!")


def run_menu(
    users: dict[int, dict],
    parameters: dict[int, dict],
    measurements: list[dict],
    items: list[dict],
) -> None:
    """Основной цикл меню."""
    while True:
        print(MENU)
        choice = input_int("Выберите действие: ")
        if choice == 0:
            return
        if choice == 1:
            show_users(users)
        elif choice == 2:
            show_parameters(parameters)
        elif choice == 3:
            found = find_parameter(parameters, input("Название: "))
            show_parameters({p["id"]: p for p in found})
        elif choice == 4:
            add_new_measurement(users, parameters, measurements)
        elif choice == 5:
            show_measurements(
                measurements, parameters, input_int("ID пользователя: "))
        elif choice == 6:
            print(build_report(
                users, parameters, measurements,
                input_int("ID пользователя: "), date.today()))
        elif choice == 7:
            item = add_item(
                items, input_int("ID пользователя: "),
                input("Название вещи: "), input("Размер: "))
            print(f"Вещь добавлена, id={item['id']}")
        elif choice == 8:
            query = input("Название вещи: ")
            for item in find_item(items, query):
                status = get_fit_status(is_item_suitable(
                    measurements, item["user_id"], item["size"]))
                print(f"{item['name']} ({item['size']}): {status}")
        elif choice == 9:
            done = remove_measurement(
                measurements, input_int("ID мерки: "))
            print("Мерка удалена" if done else "Мерка не найдена")
        else:
            print("Нет такого пункта меню")


if __name__ == "__main__":
    main()
