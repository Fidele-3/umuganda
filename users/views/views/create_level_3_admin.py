from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from admn.forms.admin3_account_form import CellAdminCreationForm
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile
from admn.models.admin import AdminHierarchy
from admn.models.sector_membership import sectorAdminMembership
from admn.models.cell_admin_membership import CellAdminMembership
from users.models.addresses import Sector, Cell  
from umuganda.utils.logging import log_admin_action


@method_decorator(login_required, name='dispatch')
class CreateAdminLevel3View(View):
    template_name = 'admin/create_admin_level3.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_level != 'sector_officer':
            messages.error(request, "Unauthorized access.")
            return redirect('sector_officer_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            membership = sectorAdminMembership.objects.get(admin=request.user)
            sector = membership.sector
        except sectorAdminMembership.DoesNotExist:
            messages.error(request, "You are not assigned to any sector.")
            return redirect('sector_officer_dashboard')

        form = CellAdminCreationForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        try:
            membership = sectorAdminMembership.objects.get(admin=request.user)
            assigned_sector = membership.sector
        except sectorAdminMembership.DoesNotExist:
            messages.error(request, "You are not assigned to any sector.")
            return redirect('sector_officer_dashboard')

        form = CellAdminCreationForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        cd = form.cleaned_data
        selected_cell = cd['assigned_cell']


        user = CustomUser.objects.create_user(
            full_names=cd['full_names'],
            email=cd['email'],
            password=cd['password'],
            phone_number=cd['phone_number'],
            user_level='cell_officer',
            national_id=cd['national_id'],
            is_active=True
        )

        UserProfile.objects.create(
            user=user,
            gender=cd['gender'],
            date_of_birth=cd['date_of_birth'],
            work=cd['work'],
            work_description=cd['work_description'],
            assigned_sector=assigned_sector,
            province=cd['province'],
            district=cd['district'],
            sector=cd['sector'],
            cell=cd['cell'],
            village=cd['village'],
            
        )

        AdminHierarchy.objects.create(
            added_by=request.user,
            admin=user
        )

        CellAdminMembership.objects.create(
            admin=user,
            cell=cd['assigned_cell']
        )

        log_admin_action(
            admin=request.user,
            action=f"Created Admin Level 3 (Cell Officer): {user.full_names}",
            action_type="admin_created",
            target_user=user
        )

        messages.success(request, "Cell Admin created and assigned successfully.")
        return redirect('sector_officer_dashboard')
