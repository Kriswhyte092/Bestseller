from django.urls import path
from .views import upload_files, process_files

urlpatterns = [
    path("", upload_files, name="upload_files"),
    path("process/", process_files, name="process_files"),
]
