from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction

from admn.forms.account_forms import SectorAdminCreationForm
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile
from admn.models.admin import AdminHierarchy
from admn.models.sector_membership import sectorAdminMembership
from sector.models.sector import AdminSector

@method_decorator(login_required, name='dispatch')
class CreateAdminLevel2View(View):
    template_name = 'admin/create_admin_level2.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_level != 'super_admin':
            messages.error(request, "You are not authorized to access this page.")
            return redirect('admin-dashboard')  
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = SectorAdminCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SectorAdminCreationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            try:
                # ✅ Get the AdminSector object
                admin_sector = cd['assigned_sector']

                # ✅ Check if sector already has an admin
                if sectorAdminMembership.objects.filter(sector=admin_sector).exists():
                    messages.error(request, f"Sector '{admin_sector}' already has an assigned admin.")
                    return render(request, self.template_name, {'form': form})

                # ✅ Optional: Prevent duplicate email being reused as admin
                if CustomUser.objects.filter(email=cd['email']).exists():
                    messages.error(request, f"An account with this email already exists.")
                    return render(request, self.template_name, {'form': form})

                with transaction.atomic():
                    # ✅ Create the admin user
                    user = CustomUser.objects.create_user(
                        full_names=cd['full_names'],
                        email=cd['email'],
                        password=cd['password'],
                        phone_number=cd['phone_number'],
                        user_level='sector_officer',
                        national_id=cd['national_id'],
                        is_active=True
                    )

                    # ✅ Create the profile
                    UserProfile.objects.create(
                        user=user,
                        gender=cd['gender'],
                        date_of_birth=cd['date_of_birth'],
                        work=cd['work'],
                        work_description=cd['work_description'],
                        assigned_sector=cd['assigned_sector'],
                        province=cd['province'],
                        district=cd['district'],
                        sector=cd['sector'],
                        cell=cd['cell'],
                        village=cd['village']
                    )

                    # ✅ Create the hierarchy and membership
                    AdminHierarchy.objects.create(
                        added_by=request.user,
                        admin=user
                    )
                    sectorAdminMembership.objects.create(
                        admin=user,
                        sector=admin_sector
                    )

                messages.success(request, "Sector Officer account created successfully.")
                return redirect('superadmin_dashboard')

            except AdminSector.DoesNotExist:
                messages.error(request, f"No AdminSector found for the selected sector: {cd['sector'].name}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")

        return render(request, self.template_name, {'form': form})
