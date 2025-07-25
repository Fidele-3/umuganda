from django import forms
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile
from users.models.addresses import Province, District, Sector, Cell, Village
from admn.models.sector_membership import sectorAdminMembership  # adjust path if needed


class CellAdminCreationForm(forms.Form):
    full_names = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    phone_number = forms.CharField(max_length=20)

    national_id = forms.CharField(max_length=16)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    work = forms.CharField(max_length=100)
    work_description = forms.CharField(widget=forms.Textarea)

    province = forms.ModelChoiceField(queryset=Province.objects.all())
    district = forms.ModelChoiceField(queryset=District.objects.none())
    sector = forms.ModelChoiceField(queryset=Sector.objects.none())
    cell = forms.ModelChoiceField(queryset=Cell.objects.none())
    village = forms.ModelChoiceField(queryset=Village.objects.none())

    assigned_cell = forms.ModelChoiceField(
        queryset=Cell.objects.none(),
        label="Assign Admin to Cell",
        help_text="Select the cell this admin will manage",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Restrict assigned_cell based on logged-in user’s sector
        if user:
            try:
                membership = sectorAdminMembership.objects.get(admin=user)
                sector_string = str(membership.sector)

                if "(" in sector_string and ")" in sector_string:
                    sector_name, rest = sector_string.split("(", 1)
                    sector_name = sector_name.strip()
                    district_name, province_name = rest.strip(")").split(",")
                    district_name = district_name.strip()
                    province_name = province_name.strip()

                    province = Province.objects.get(name=province_name)
                    district = District.objects.get(name=district_name, province=province)
                    sector = Sector.objects.get(name=sector_name, district=district)

                    self.fields['assigned_cell'].queryset = Cell.objects.filter(sector=sector)
                else:
                    self.fields['assigned_cell'].queryset = Cell.objects.none()

            except Exception:
                self.fields['assigned_cell'].queryset = Cell.objects.none()

        # ✅ Cascading dropdown logic
        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['district'].queryset = District.objects.filter(province_id=province_id)
            except (ValueError, TypeError):
                pass

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['sector'].queryset = Sector.objects.filter(district_id=district_id)
            except (ValueError, TypeError):
                pass

        if 'sector' in self.data:
            try:
                sector_id = int(self.data.get('sector'))
                self.fields['cell'].queryset = Cell.objects.filter(sector_id=sector_id)
            except (ValueError, TypeError):
                pass

        if 'cell' in self.data:
            try:
                cell_id = int(self.data.get('cell'))
                self.fields['village'].queryset = Village.objects.filter(cell_id=cell_id)
            except (ValueError, TypeError):
                pass

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")
        return email

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if CustomUser.objects.filter(national_id=national_id).exists():
            raise forms.ValidationError("National ID is already registered")
        return national_id

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        cleaned_data['password'] = password1
        return cleaned_data
