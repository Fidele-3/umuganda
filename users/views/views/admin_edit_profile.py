# user/views/profile_edit_view.py

from django.shortcuts import render, redirect
from django.contrib import messages
from admn.forms.admin_edit_profile import AdminProfileForm
from users.models.userprofile import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def edit_admin_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('admin_profile')  # your profile view name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AdminProfileForm(instance=profile)

    return render(request, 'admin/edit_profile.html', {'form': form})
