from django.shortcuts import render, redirect, get_object_or_404
from .models import Announcement, FrontPageImage
from .forms import AnnouncementForm, ImageUploadForm
from django.http import JsonResponse


def announcement_list(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        announcements = list(Announcement.objects.values("title", "content"))
        return JsonResponse(announcements, safe=False)
    else:
        announcements = Announcement.objects.all()
        images = FrontPageImage.objects.all()
        return render(
            request,
            "announcements/list.html", 
            {"announcements": announcements, "images": images}
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


def frontpage_images(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        images = FrontPageImage.objects.all()  # Fetch all images
        image_urls = [image.image.url for image in images]  # Get URLs for all images
        return JsonResponse({"images": image_urls})  # Return as a JSON array
    else:
        return JsonResponse({"image_url": None})


def delete_image(request, image_id):
    image = get_object_or_404(FrontPageImage, id=image_id)
    if request.method == "POST":
        image.delete()
        return redirect('announcement_list')  # Redirect to the correct view
    return render(request, 'confirm_delete.html', {'image': image})