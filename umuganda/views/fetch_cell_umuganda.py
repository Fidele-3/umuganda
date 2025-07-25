from django.shortcuts import render
from django.utils import timezone
from umuganda.models import UmugandaSession

def cell_officer_dashboard(request):
    profile = request.user.profile  
    cell = profile.cell
    sector = cell.sector

    today = timezone.now().date()

    
    session = UmugandaSession.objects.filter(
        sector=sector,
        cell=cell,
        date__gte=today
    ).order_by('date').first()  

    context = {
        'umuganda_session': session,  
    }

    return render(request, 'admin/admin_level3_dashboard.html', context)
