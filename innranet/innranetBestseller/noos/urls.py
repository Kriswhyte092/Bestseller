from django.urls import path
from .views import noos

urlpatterns = [
    path("", noos, name="noos"),
]
