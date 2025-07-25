# user/views/request_otp_form.py

from django.shortcuts import render, redirect
from admn.forms.request_otp import RequestOTPForm
from users.models import CustomUser, PasswordResetOTP
from django.utils import timezone
from datetime import timedelta
from umuganda.utils.generate_otp import generate_otp
from users.tasks.otp_notification import send_email_password_reset_otp
from django.urls import reverse

# user/views/request_otp_form.py

def request_password_otp_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            email = request.user.email
            form = RequestOTPForm(request.POST, user_email=email, disable_email=True)
        else:
            form = RequestOTPForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            try:
                user = CustomUser.objects.get(email=email)
                otp = generate_otp()
                expires_at = timezone.now() + timedelta(minutes=15)

                PasswordResetOTP.objects.create(
                    user=user,
                    otp_code=otp,
                    expires_at=expires_at
                )

                request.session["reset_email"] = email
                request.session["reset_otp"] = otp

                send_email_password_reset_otp.delay(
                    user_id=str(user.id),
                    full_names=user.full_names,
                    email=user.email,
                    otp_code=otp,
                    reset_link=request.build_absolute_uri(
                        reverse("password-reset-final")
                    )
                )

                return redirect("verify-reset-otp")

            except CustomUser.DoesNotExist:
                form.add_error("email", "User with this email does not exist.")
    else:
        if request.user.is_authenticated:
            form = RequestOTPForm(user_email=request.user.email, disable_email=True)
        else:
            form = RequestOTPForm()

    return render(request, "admin/request_otp.html", {"form": form})
