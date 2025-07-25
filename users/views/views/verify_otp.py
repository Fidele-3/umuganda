# user/views/reset_password.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from admn.forms.verify_otp import VerifyResetOTPForm
from users.models import CustomUser, PasswordResetOTP

def verify_reset_otp_view(request):
    email = request.session.get("reset_email")
    if not email:
        messages.error(request, "Session expired. Please request a new OTP.")
        return redirect("password-reset-otp")

    if request.method == "POST":
        form = VerifyResetOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            try:
                user = CustomUser.objects.get(email=email)
                latest_otp = PasswordResetOTP.objects.filter(user=user).latest("created_at")

                if latest_otp.otp_code != otp:
                    form.add_error("otp", "Invalid OTP.")
                elif latest_otp.expires_at < timezone.now():
                    form.add_error("otp", "OTP has expired.")
                else:
                    
                    latest_otp.is_used = True
                    latest_otp.save()
                    request.session["otp_verified"] = True  # ✅ Flag for next step
                    return redirect("password-reset-final")
            except (CustomUser.DoesNotExist, PasswordResetOTP.DoesNotExist):
                messages.error(request, "Verification failed. Please request a new OTP.")
                return redirect("request_otp_form")
    else:
        form = VerifyResetOTPForm()

    return render(request, "admin/verify_otp.html", {"form": form})
