from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Announcement
from .forms import AnnouncementForm


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

# Edit Announcement
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

# Delete Announcement
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'announcement': announcement})