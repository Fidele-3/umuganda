from django import forms
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile
from sector.models.sector import AdminSector as AgencySector
from users.models.addresses import Province, District, Sector, Cell, Village

class SectorAdminCreationForm(forms.Form):
    # User account data
    full_names = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # Profile data
    national_id = forms.CharField(max_length=16)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1970, 2025)))
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)
    work = forms.CharField(max_length=50, required=False)
    work_description = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=20)
    assigned_sector = forms.ModelChoiceField(queryset=AgencySector.objects.all())

    province = forms.ModelChoiceField(queryset=Province.objects.all())
    district = forms.ModelChoiceField(queryset=District.objects.all())
    sector = forms.ModelChoiceField(queryset=Sector.objects.all())
    cell = forms.ModelChoiceField(queryset=Cell.objects.all())
    village = forms.ModelChoiceField(queryset=Village.objects.all())

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")
        return email

    def clean_full_names(self):
        full_names = self.cleaned_data['full_names']
        if CustomUser.objects.filter(full_names=full_names).exists():
            raise forms.ValidationError("full_names already exists")
        return full_names

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if CustomUser.objects.filter(national_id=national_id).exists():
            raise forms.ValidationError("National ID is already registered")
        return national_id

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            cleaned_data['password'] = password1  # Final unified password value

        return cleaned_data
