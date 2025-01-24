from django.urls import path
from .views import noos, noos_info, noos_products

urlpatterns = [
    path("noos-info/", noos_info, name="noos_info"),
    path('', noos_products, name='noos-products'),  # Map to /noos/
]