"""Тесты веб-страниц (ПР5): маршруты, view-функции, коды ответов."""
from pathlib import Path

import pytest
from django.test import Client, override_settings
from django.urls import reverse

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def client():
    return Client()


@pytest.mark.parametrize("url", [
    "/", "/parameters/", "/parameters/1/", "/measurements/",
    "/measurements/1/", "/items/", "/items/1/",
])
def test_pages_open(client, url):
    assert client.get(url).status_code == 200


@pytest.mark.parametrize("url", [
    "/parameters/999/", "/measurements/999/", "/items/999/",
    "/nonexistent/",
])
def test_missing_objects_return_404(client, url):
    assert client.get(url).status_code == 404


def test_parameter_page_shows_data(client):
    text = client.get("/parameters/1/").content.decode()
    assert "Обхват груди" in text
    assert "см" in text


def test_measurement_page_shows_related_objects(client):
    text = client.get("/measurements/1/").content.decode()
    assert "Алексей Семенов" in text
    assert "Обхват груди" in text


def test_item_page_shows_fit_status(client):
    text = client.get("/items/1/").content.decode()
    assert "Куртка зимняя" in text
    assert "размеру" in text


@override_settings(DEBUG=False)
def test_custom_404_page(client):
    text = client.get("/nonexistent/").content.decode()
    assert "404" in text
    assert "На главную" in text


# ---- ПР6: шаблоны, include, namespace, статика ----

def test_pages_use_base_template(client):
    text = client.get("/parameters/").content.decode()
    assert "<nav" in text
    assert "bootstrap@5.3.3" in text
    assert "/static/css/main.css" in text
    assert "/static/js/main.js" in text


def test_navigation_links_built_by_url_names(client):
    text = client.get("/").content.decode()
    for url in ("/parameters/", "/measurements/", "/items/"):
        assert f'href="{url}"' in text


@pytest.mark.parametrize("name, args, expected", [
    ("homepage:index", [], "/"),
    ("parameters:list", [], "/parameters/"),
    ("parameters:detail", [2], "/parameters/2/"),
    ("measurements:list", [], "/measurements/"),
    ("measurements:detail", [3], "/measurements/3/"),
    ("items:list", [], "/items/"),
    ("items:detail", [1], "/items/1/"),
])
def test_reverse_namespaced_urls(name, args, expected):
    assert reverse(name, args=args) == expected


def test_list_pages_show_counts_via_length_filter(client):
    assert "Всего параметров: 4" in client.get(
        "/parameters/").content.decode()
    assert "Всего мерок: 3" in client.get(
        "/measurements/").content.decode()
    assert "Всего вещей: 2" in client.get("/items/").content.decode()


def test_list_item_rows_are_included_partials(client):
    text = client.get("/items/").content.decode()
    assert text.count('class="list-group-item') == 2


def test_measurement_badge_depends_on_range(client):
    text = client.get("/measurements/1/").content.decode()
    assert "в допустимых пределах" in text


def test_static_files_exist():
    for name in ("css/main.css", "js/main.js", "img/logo.png"):
        assert (BASE_DIR / "static" / name).is_file()


def test_templates_exist():
    for name in ("base.html", "includes/navigation.html", "404.html"):
        assert (BASE_DIR / "templates" / name).is_file()


# ---- ПР7: страницы, читающие данные из SQLite ----

def test_statistics_page(client):
    text = client.get("/statistics/").content.decode()
    assert "Статистика" in text
    assert "Мерки по параметрам" in text
    assert "Алексей Семенов: 2" in text


def test_by_date_page_without_date_lists_dates(client):
    text = client.get("/measurements/by-date/").content.decode()
    assert "2026-09-15" in text


def test_by_date_page_finds_measurements(client):
    url = "/measurements/by-date/?date=2026-09-15"
    text = client.get(url).content.decode()
    assert "Найдено мерок за 2026-09-15: 2" in text


def test_by_date_page_empty_result(client):
    url = "/measurements/by-date/?date=2000-01-01"
    text = client.get(url).content.decode()
    assert "За эту дату мерок нет" in text


def test_items_page_reads_from_database(client):
    text = client.get("/items/2/").content.decode()
    assert "Платье летнее" in text
    assert "Мария Иванова" in text
