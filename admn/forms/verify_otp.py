# user/forms.py

from django import forms

class VerifyResetOTPForm(forms.Form):
    otp = forms.CharField(
        label="Enter the 6-digit OTP",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={"placeholder": "e.g. 123456", "autocomplete": "off"})
    )
