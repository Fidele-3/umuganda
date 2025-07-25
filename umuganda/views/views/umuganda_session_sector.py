# umuganda/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from umuganda.forms.umuganda_creation_form import UmugandaSessionForm
from umuganda.models import UmugandaSession

@login_required
def create_umuganda_session(request):
    user = request.user

   
    if not user.user_level == 'sector_officer':
        messages.error(request, "You are not authorized to create Umuganda sessions.")
        return redirect('dashboard')  # adjust if needed

    # Get sector from sectorAdminMembership
    sector_membership = getattr(user, 'sector_membership', None)
    if not sector_membership or not sector_membership.sector:
        messages.error(request, "Your assigned sector is missing.")
        return redirect('dashboard')

    sector = sector_membership.sector

    if request.method == 'POST':
        form = UmugandaSessionForm(request.POST)
        if form.is_valid():
            umuganda_session = form.save(commit=False)
            umuganda_session.sector = sector.sector
            umuganda_session.created_by = user
            umuganda_session.save()
            messages.success(request, "Umuganda session created successfully.")
            return redirect('sector_officer_dashboard')  
    else:
        form = UmugandaSessionForm()

    return render(request, 'admin/create_session.html', {
        'form': form,
        'sector': sector.sector.name
    })
