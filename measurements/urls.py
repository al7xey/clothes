from django.urls import path

from . import views

urlpatterns = [
    path("", views.measurements, name="measurements"),
    path("<int:value_id>/", views.measurement_detail,
         name="measurement_detail"),
]
