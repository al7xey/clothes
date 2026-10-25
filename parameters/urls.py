from django.urls import path

from . import views

urlpatterns = [
    path("", views.parameters, name="parameters"),
    path("<int:parameter_id>/", views.parameter_detail,
         name="parameter_detail"),
]
