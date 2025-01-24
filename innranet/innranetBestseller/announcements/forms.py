from django import forms
from .models import Announcement, FrontPageImage


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "content"]


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = FrontPageImage
        fields = ["image"]
