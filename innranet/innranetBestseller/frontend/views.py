from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Announcement
from .forms import AnnouncementForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'frontend/index.html', {'announcements': announcements})

def loginn(request):
    if request.method=='POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(f"LOGIN: User: {fnm} Password: {pwd}")
        user=authenticate(request,username=fnm, password=pwd)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return redirect('/login')
    
    return render(request, 'login.html')

def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AnnouncementForm()
    return render(request, 'create_announcement.html', {'form': form})

def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'edit_announcement.html', {'form': form})

def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'announcement': announcement})

@csrf_exempt
def edit_announcement_ajax(request):
    if request.method == 'POST':
        announcement_id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        Announcement.objects.filter(id=announcement_id).update(title=title, content=content)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@csrf_exempt
def delete_announcement_ajax(request):
    if request.method == 'POST':
        announcement_id = request.POST.get('id')
        Announcement.objects.filter(id=announcement_id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)