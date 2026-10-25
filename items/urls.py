from django.urls import path

from . import views

urlpatterns = [
    path("", views.items, name="items"),
    path("<int:item_id>/", views.item_detail, name="item_detail"),
]
