from django.http import HttpResponse


def page(title, content):
    """Общий каркас HTML-страницы: Bootstrap и навигация."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/parameters/">Параметры</a>
        <a class="nav-link" href="/measurements/">Мерки</a>
        <a class="nav-link" href="/items/">Вещи</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Система учета размеров одежды</h1>
    <p class="lead">Учет мерок пользователей и подбор размера вещей.</p>
    <p>Основные разделы:</p>
    <a href="/parameters/" class="btn btn-primary me-2">Параметры</a>
    <a href="/measurements/" class="btn btn-secondary me-2">Мерки</a>
    <a href="/items/" class="btn btn-success">Вещи</a>
    """
    return HttpResponse(page("Учет размеров одежды", content))


def page_not_found(request, exception):
    """Собственная страница ошибки 404."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
