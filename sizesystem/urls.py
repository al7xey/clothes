"""Корневая конфигурация маршрутов проекта."""
from django.contrib import admin
from django.urls import include, path

from homepage.views import catch_all_404

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("parameters/", include("parameters.urls")),
    path("measurements/", include("measurements.urls")),
    path("items/", include("items.urls")),
    path("<path:unmatched_path>", catch_all_404),
]

handler404 = "homepage.views.page_not_found"
