from django.urls import path
from .views import product_info

urlpatterns = [
    path('noos-info/', product_info, name='product_info'),
]