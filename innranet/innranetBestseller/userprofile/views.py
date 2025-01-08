from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    user = request.user
    user_profile = getattr(
        user, "userprofile", None
    )  # Optional if using the extended model
    context = {
        "username": user.username,
        "access_level": user_profile.access_level if user_profile else "N/A",
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }
    return render(request, "userprofile/profile.html", context)
