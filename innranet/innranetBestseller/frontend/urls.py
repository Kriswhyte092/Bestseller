from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('NOOS', views.index),
    path('bonus', views.index),
    path('login/', views.loginn),
]
