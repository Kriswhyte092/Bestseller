from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FrontPageImage(models.Model):
    image = models.ImageField(upload_to="frontpage_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
