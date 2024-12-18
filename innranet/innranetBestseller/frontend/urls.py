from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('NOOS', views.index),
    path('bonus', views.index),
    path('login/', views.loginn),
    path('create/', views.create_announcement, name='create_announcement'),
    path('edit/<int:pk>/', views.edit_announcement, name='edit_announcement'),
    path('delete/<int:pk>/', views.delete_announcement, name='delete_announcement'),
    path('edit-announcement-ajax/', views.edit_announcement_ajax, name='edit_announcement_ajax'),
    path('delete-announcement-ajax/', views.delete_announcement_ajax, name='delete_announcement_ajax'),
]
