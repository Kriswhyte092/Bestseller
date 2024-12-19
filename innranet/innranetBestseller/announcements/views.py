from django.shortcuts import render, redirect
from .models import Announcement, FrontPageImage
from .forms import AnnouncementForm, ImageUploadForm


from django.http import JsonResponse
from .models import Announcement


def announcement_list(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        announcements = list(Announcement.objects.values("title", "content"))
        return JsonResponse(announcements, safe=False)
    else:
        announcements = Announcement.objects.all()
        return render(
            request, "announcements/list.html", {"announcements": announcements}
        )


def create_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("announcement_list")
    else:
        form = AnnouncementForm()
    return render(request, "announcements/create.html", {"form": form})


def delete_announcement(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    announcement.delete()
    return redirect("announcement_list")


def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("announcement_list")
    else:
        form = ImageUploadForm()
    return render(request, "announcements/upload_image.html", {"form": form})


from .models import FrontPageImage


def frontpage_image(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        image = FrontPageImage.objects.last()  # Get the latest uploaded image
        if image and image.image:  # Check if an image exists
            return JsonResponse(
                {"image_url": image.image.url}
            )  # Return the correct URL
        else:
            return JsonResponse({"image_url": None})
