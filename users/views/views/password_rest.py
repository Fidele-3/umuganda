# user/views/reset_password.py

from django.contrib.auth.hashers import make_password
from admn.forms.reset_passord import FinalPasswordResetForm
from django.shortcuts import render, redirect
from django.contrib import messages 
from users.models import CustomUser

def final_password_reset_view(request):
    email = request.session.get("reset_email")
    otp_verified = request.session.get("otp_verified")

    if not email or not otp_verified:
        messages.error(request, "Unauthorized access or session expired.")
        return redirect("request_otp_form")

    if request.method == "POST":
        form = FinalPasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            try:
                user = CustomUser.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()

                # Clear session flags after success
                request.session.pop("reset_email", None)
                request.session.pop("otp_verified", None)

                messages.success(request, "Password reset successfully. You can now log in.")
                return redirect("admin_login")  # Adjust to your login URL name
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect("request_otp_form")
    else:
        form = FinalPasswordResetForm()

    return render(request, "admin/password_reset.html", {"form": form})
