# Система учета размеров одежды

Консольное приложение для учета мерок пользователей и размеров их вещей.
Приложение позволяет вводить значения параметров (обхват груди, талии,
бёдер, рост), подбирать буквенный размер и проверять, подходит ли вещь.

## Назначение
Помогает не ошибаться с размером при покупке одежды и вести учет размеров
всех членов семьи.

## Целевая аудитория
Покупатели одежды онлайн и семьи, которые ведут учет размеров домочадцев.

## Предметная область
Розничная торговля одеждой и личный учет одежды. Размер вещи определяется
набором параметров (мерок) и их значений.

## Основные сущности
Предметная область представлена классами; все они наследуют базовый класс
`Entity` (идентификатор `id` только для чтения и метод `to_dict()`).

### Parameter — параметр
Измеряемая характеристика (обхват груди, талии, бёдер, рост).

Атрибуты: `id`, `name`, `unit`, `min_value`, `max_value`.

Методы:
- `is_value_valid(amount)` — значение в допустимых пределах;
- `validate_range(min_value, max_value)` — `@staticmethod`, проверка диапазона;
- `from_data(data)` — `@classmethod`, создание объекта из JSON-данных;
- `to_dict()`, `__str__()`.

### User — пользователь
Атрибуты: `id`, `name`, `email`.

Методы: `from_data(data)` (`@classmethod`), `to_dict()`, `__str__()`.

### Value — значение мерки
Результат измерения параметра у пользователя. Хранит **ссылки на объекты**
`User` и `Parameter` (композиция), а не только их идентификаторы.

Атрибуты: `id`, `user`, `parameter`, `amount`, `value_date`.

Методы: `is_in_range()`, `to_dict()` (ссылки заменяются на `user_id`
и `parameter_id`), `__str__()`.

### Item — вещь
Атрибуты: `id`, `user`, `name`, `size`.

Методы:
- `recommend_size(chest)` — `@staticmethod`, подбор размера по обхвату груди;
- `is_suitable_for(chest)` — подходит ли вещь при данном обхвате груди;
- `to_dict()`, `__str__()`.

## Взаимодействие объектов

    Item  ──→ User ←── Value ──→ Parameter

`Value` и `Item` содержат ссылки на `User`; `Value` связан с `Parameter`.
Данные связанных объектов доступны напрямую: `value.user.name`,
`value.parameter.unit`, `item.user.email`.

## Основные операции
- просмотр пользователей, параметров и вещей;
- поиск параметра по названию, фильтрация и сортировка;
- добавление мерки с проверкой допустимых пределов;
- запрет второй мерки одного параметра на одну дату;
- просмотр и удаление мерок пользователя;
- подбор размера и отчёт, проверка вещи по размеру.

## Хранение данных
Данные лежат в `data/*.json` (формат тот же, что в ПР2). При загрузке
записи JSON преобразуются в объекты `User`, `Parameter`, `Value`, `Item`:
по `user_id` и `parameter_id` находятся связанные объекты. При сохранении
объекты преобразуются обратно в данные, а ссылки — в идентификаторы.
Если связанный объект не найден, загрузка завершается ошибкой.

## Структура проекта

    clothing_size_system/
    ├── README.md
    ├── requirements.txt
    ├── pytest.ini
    ├── .flake8
    ├── manage.py
    ├── sizesystem/        (Django-проект)
    ├── homepage/ parameters/ measurements/ items/  (Django-приложения)
    ├── main.py
    ├── storage.py
    ├── utils.py
    ├── models/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── parameters.py
    │   ├── users.py
    │   ├── values.py
    │   └── items.py
    ├── data/
    │   ├── users.json
    │   ├── parameters.json
    │   ├── measurements.json
    │   └── items.json
    └── tests/
        ├── test_parameters.py
        ├── test_users.py
        ├── test_values.py
        ├── test_items.py
        └── test_storage.py

## Назначение модулей
- `main.py` — точка входа, меню, сценарии;
- `models/` — классы и функции обработки коллекций объектов;
- `storage.py` — преобразование JSON ↔ объекты;
- `utils.py` — безопасный ввод чисел и дат;
- `tests/` — автоматизированные тесты.

## Требования
- Python 3.10+;
- pytest;
- flake8.

Установка зависимостей:

    pip install -r requirements.txt

## Запуск программы

    python main.py

## Тестирование
Тесты проверяют создание объектов, атрибуты, `__str__`, методы классов,
правило «одна мерка параметра на дату», связи объектов и загрузку/сохранение
JSON:

    pytest -v

## Проверка качества кода

    flake8

## Веб-интерфейс на Django (ПР5)
Консольное приложение (ПР1–ПР3) сохранено. Рядом создан веб-интерфейс на
Django 5.2: страницы показывают данные из JSON-файлов, используя классы
`Parameter`, `User`, `Value`, `Item` и функции пакета `models/`.

### Django-проект и приложения
- `sizesystem/` — пакет конфигурации проекта (`settings.py`, `urls.py`);
- `homepage` — главная страница, общий каркас страниц `page()`, страница 404;
- `parameters` — параметры (мерки): список и страница параметра;
- `measurements` — значения мерок пользователей: список и страница мерки;
- `items` — вещи: список и страница вещи с проверкой размера.

Для пользователей отдельное приложение не создаётся: пользователь отображается
как владелец мерки и вещи (`value.user.name`, `item.user.name`).

### Страницы и адреса
| Страница | URL | View-функция |
|---|---|---|
| Главная | `/` | `homepage.views.index` |
| Список параметров | `/parameters/` | `parameters.views.parameters` |
| Параметр | `/parameters/<id>/` | `parameters.views.parameter_detail` |
| Список мерок | `/measurements/` | `measurements.views.measurements` |
| Мерка | `/measurements/<id>/` | `measurements.views.measurement_detail` |
| Список вещей | `/items/` | `items.views.items` |
| Вещь | `/items/<id>/` | `items.views.item_detail` |

Для несуществующего идентификатора возвращается страница с кодом 404.
Неизвестные адреса обрабатывает `handler404` (`homepage.views.page_not_found`).
Оформление: HTML и Bootstrap 5.3 (CDN).

### Запуск веб-приложения

    py -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

После запуска откройте http://127.0.0.1:8000/. Консольная версия запускается
командой `python main.py`.

## Шаблоны Django (ПР6)

HTML больше не собирается в Python-коде: view-функции передают данные
в шаблоны через `render()`.

- `templates/base.html` – базовый шаблон (Bootstrap, подключение статики,
  блоки `title` и `content`, подвал с текущим годом);
- `templates/includes/navigation.html` – меню, подключаемое через `include`;
- `templates/404.html` – собственная страница ошибки 404;
- `<приложение>/templates/<приложение>/` – шаблоны `list.html`,
  `detail.html` и частичные шаблоны в `includes/`;
- `static/css/main.css`, `static/js/main.js`, `static/img/logo.png` –
  статические файлы.

Используются теги `extends`, `block`, `include`, `url`, `static`, `for ... empty`,
`if / elif / else`, фильтры `length` и `default`. Имена маршрутов имеют
пространства имён: `homepage:index`, `parameters:list`, `parameters:detail`,
`measurements:list`, `measurements:detail`, `items:list`, `items:detail`.

## База данных SQLite (ПР7)

Данные веб-приложения хранятся в файле `data/clothes.sqlite`
(таблицы `users`, `parameters`, `measurements`, `items` со связями
через внешние ключи).

- `sql/schema.sql` – создание таблиц и индексов;
- `sql/queries.sql` – именованные SQL-запросы (выборки, `WHERE`, `JOIN`,
  `COUNT`, `GROUP BY`, `HAVING`);
- `db/database.py` – подключение (`sqlite3.Row`, внешние ключи включены),
  загрузка запросов и функции `fetch_all`, `fetch_one`, `fetch_value`;
- `db/import_json.py` – перенос данных из JSON в базу.

Запросы выполняются только с параметрами (`?`), без подстановки строк.
Пересоздать базу из JSON: `python -m db.import_json`.

Новые страницы: `/measurements/by-date/?date=2026-09-15` (мерки по дате) и
`/statistics/` (количество записей и группировки).

## План развития
- реализация пользователей;
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
