from django.shortcuts import render, redirect, get_object_or_404
from .models import Info
from .forms import InfoForm


# View to display all information
def info_list(request):
    infos = Info.objects.all()
    return render(request, "info/info_list.html", {"infos": infos})


# View to add new information
def add_info(request):
    if request.method == "POST":
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("info_list")
    else:
        form = InfoForm()
    return render(request, "info/add_info.html", {"form": form})


# View to edit existing information
def edit_info(request, pk):
    info = get_object_or_404(Info, pk=pk)
    if request.method == "POST":
        form = InfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect("info_list")
    else:
        form = InfoForm(instance=info)
    return render(request, "info/edit_info.html", {"form": form, "info": info})
