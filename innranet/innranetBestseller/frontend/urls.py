from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from .views import debug_session

urlpatterns = [
    path("", views.index),
    path("staff", views.staff, name="staff"),
    path("NOOS", views.index, name="noos"),
    path("bonus", views.index),
    path("login/", views.loginn),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", include("userprofile.urls")),
    path('debug_session/', debug_session),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
