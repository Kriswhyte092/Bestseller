from django.urls import path
from . import views

urlpatterns = [
    path("", views.info_list, name="info_list"),
    path("add/", views.add_info, name="add_info"),
    path("edit/<int:pk>/", views.edit_info, name="edit_info"),
]
