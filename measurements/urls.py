from django.urls import path

from . import views

app_name = "measurements"

urlpatterns = [
    path("", views.measurements, name="list"),
    path("by-date/", views.measurements_by_date, name="by_date"),
    path("<int:value_id>/", views.measurement_detail, name="detail"),
]
