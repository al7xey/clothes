"""Система учета размеров одежды — консольное приложение (ПР3, ООП)."""
from datetime import date
from typing import List

from models import Item, Parameter, User, Value
from models.items import (
    CHEST_PARAMETER_ID, add_item, find_item, get_fit_status,
    is_item_suitable, show_items,
)
from models.parameters import (
    find_parameter, get_parameter_by_id, show_parameters,
)
from models.users import get_user_by_id, show_users
from models.values import (
    add_value, get_latest_amount, remove_value, show_values,
)
from storage import (
    DATA_DIR, load_items, load_parameters, load_users, load_values,
    save_items, save_parameters, save_users, save_values,
)
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
10. Показать вещи
0. Выход"""


def build_report(
    values: List[Value],
    user: User,
    chest: Parameter,
    report_date: date,
) -> str:
    """Отчёт по обхвату груди пользователя (функция из ПР1)."""
    amount = get_latest_amount(values, user, chest)
    if amount is None:
        return "Недостаточно данных для отчёта"
    return (
        f"Пользователь: {user.name}\n"
        f"Дата отчёта: {report_date}\n"
        f"{chest.name}: {amount} {chest.unit}\n"
        f"Рекомендуемый размер: {Item.recommend_size(amount)}"
    )


def create_new_value(
    users: List[User], parameters: List[Parameter], values: List[Value]
) -> None:
    """Сценарий добавления мерки: найти User и Parameter, создать Value."""
    user = get_user_by_id(users, input_int("ID пользователя: "))
    if user is None:
        print("Пользователь не найден")
        return
    parameter = get_parameter_by_id(parameters, input_int("ID параметра: "))
    if parameter is None:
        print("Параметр не найден")
        return
    amount = input_float("Значение: ")
    value_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    value = add_value(values, user, parameter, amount, value_date)
    if value is None:
        print("Мерка не добавлена: значение вне допустимых пределов "
              "или мерка на эту дату уже есть")
    else:
        print(f"Мерка добавлена, id={value.id}")


def check_items(
    values: List[Value], items: List[Item], chest: Parameter
) -> None:
    """Проверить, подходят ли найденные вещи владельцам."""
    for item in find_item(items, input("Название вещи: ")):
        status = get_fit_status(is_item_suitable(values, item, chest))
        print(f"{item}: {status}")


def run_menu(
    users: List[User],
    parameters: List[Parameter],
    values: List[Value],
    items: List[Item],
) -> None:
    """Основной цикл меню."""
    chest = get_parameter_by_id(parameters, CHEST_PARAMETER_ID)
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
            show_parameters(find_parameter(parameters, input("Название: ")))
        elif choice == 4:
            create_new_value(users, parameters, values)
        elif choice in (5, 6, 7):
            user = get_user_by_id(users, input_int("ID пользователя: "))
            if user is None:
                print("Пользователь не найден")
            elif choice == 5:
                show_values(values, user)
            elif choice == 6:
                print(build_report(values, user, chest, date.today()))
            else:
                item = add_item(
                    items, user, input("Название вещи: "), input("Размер: "))
                print(f"Вещь добавлена, id={item.id}")
        elif choice == 8:
            check_items(values, items, chest)
        elif choice == 9:
            done = remove_value(values, input_int("ID мерки: "))
            print("Мерка удалена" if done else "Мерка не найдена")
        elif choice == 10:
            show_items(items)
        else:
            print("Нет такого пункта меню")


def main() -> None:
    """Точка запуска: загрузка объектов, меню, сохранение."""
    try:
        users = load_users(f"{DATA_DIR}/users.json")
        parameters = load_parameters(f"{DATA_DIR}/parameters.json")
        values = load_values(
            f"{DATA_DIR}/measurements.json", users, parameters)
        items = load_items(f"{DATA_DIR}/items.json", users)
    except ValueError as error:
        print(f"Не удалось загрузить данные: {error}")
        return
    try:
        run_menu(users, parameters, values, items)
    except (EOFError, KeyboardInterrupt):
        print("\nВвод прерван")
    save_users(f"{DATA_DIR}/users.json", users)
    save_parameters(f"{DATA_DIR}/parameters.json", parameters)
    save_values(f"{DATA_DIR}/measurements.json", values)
    save_items(f"{DATA_DIR}/items.json", items)
    print("Данные сохранены. До свидания!")


if __name__ == "__main__":
    main()
