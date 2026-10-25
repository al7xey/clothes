"""Тесты веб-страниц (ПР5): маршруты, view-функции, коды ответов."""
import pytest
from django.test import Client, override_settings


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
