from django.urls import path
from .views import product_info, noos

urlpatterns = [
    path("", noos, name="noos"),
    path("noos-info/", product_info, name="product_info"),
]
