from django.urls import path
from . import views

urlpatterns = [
    path("", views.announcement_list, name="announcement_list"),
    path("create/", views.create_announcement, name="create_announcement"),
    path("delete/<int:pk>/", views.delete_announcement, name="delete_announcement"),
    path("upload_image/", views.upload_image, name="upload_image"),
    path("images/", views.frontpage_images, name="frontpage_images"),
]
