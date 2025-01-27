from django.urls import path
from .views import noos, noos_info

urlpatterns = [
    path("", noos, name="noos"),
    path("noos-info/", noos_info, name="noos_info"),
]