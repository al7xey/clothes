from django.urls import path

from . import views

app_name = "measurements"

urlpatterns = [
    path("", views.measurements, name="list"),
    path("<int:value_id>/", views.measurement_detail, name="detail"),
]
