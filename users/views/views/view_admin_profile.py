# admin_panel/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users.models import UserProfile

@login_required
def view_admin_profile(request):
    user = request.user
    try:
        profile = user.profile  # related_name='profile' in UserProfile
    except UserProfile.DoesNotExist:
        profile = None  # fallback if profile is missing (should rarely happen)

    return render(request, 'admin/view_profile.html', {
        'user': user,
        'profile': profile
    })
