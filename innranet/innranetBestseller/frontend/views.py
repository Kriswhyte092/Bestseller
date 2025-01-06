from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    return render(request, "frontend/index.html")


@unauthenticated_user
def loginn(request):
    if request.method == "POST":
        fnm = request.POST.get("fnm")
        pwd = request.POST.get("pwd")
        print(f"LOGIN: User: {fnm} Password: {pwd}")
        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/login")

    return render(request, "login.html")
