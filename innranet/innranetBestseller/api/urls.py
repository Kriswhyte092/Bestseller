from django.urls import path
from .views import NOOSview 

urlpatterns = [
    path('home', NOOSview.as_view()) 
]
