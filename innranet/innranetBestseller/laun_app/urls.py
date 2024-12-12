from django.urls import path
from . import views

from django.shortcuts import render

def index(request):
    return render(request, "laun_app/upload.html")

urlpatterns = [
    path("", index, name="laun_index"),  # Add a default view for `/laun/`
    
    path("process/", views.process_data_file, name="process_data_file"),
]
