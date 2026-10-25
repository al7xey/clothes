from django.urls import path

from . import views

app_name = "parameters"

urlpatterns = [
    path("", views.parameters, name="list"),
    path("<int:parameter_id>/", views.parameter_detail, name="detail"),
]
