from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_level = models.CharField(
        max_length=50,
        choices=[("admin", "Admin"), ("editor", "Editor"), ("viewer", "Viewer")],
    )

    def __str__(self):
        return self.user.username
