"""Корневая конфигурация маршрутов проекта."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("parameters/", include("parameters.urls")),
    path("measurements/", include("measurements.urls")),
    path("items/", include("items.urls")),
]

handler404 = "homepage.views.page_not_found"
