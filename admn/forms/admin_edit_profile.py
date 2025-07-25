# user/forms/profile_form.py

from django import forms
from users.models.userprofile import UserProfile

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'created_at', 'updated_at']
