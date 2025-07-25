# admn/forms/request_otp.py

from django import forms

class RequestOTPForm(forms.Form):
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    def __init__(self, *args, user_email=None, disable_email=False, **kwargs):
        super().__init__(*args, **kwargs)
        if user_email:
            self.fields["email"].initial = user_email
        if disable_email:
            self.fields["email"].widget.attrs["readonly"] = True
            self.fields["email"].widget.attrs["style"] = "background-color: #f0f0f0;"  # optional: show it's readonly
