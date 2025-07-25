from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from admn.forms.forms import sectorCreateForm
from umuganda.utils.logging import log_admin_action

@login_required
def create_sector_view(request):
    if request.user.user_level != 'super_admin':
        print("AUTHORIZATION ERROR: Non-super_admin tried to access sector creation.")
        return redirect('unauthorized')

    if request.method == 'POST':
        print("==== RECEIVED POST REQUEST ====")
        print("POST DATA:", dict(request.POST))
        print("FILES:", dict(request.FILES))

        form = sectorCreateForm(request.POST, request.FILES)

        if form.is_valid():
            sector = form.save()
            print(f"SECTOR CREATED: {sector.sector.name} (ID: {sector.id})")

            log_admin_action(
                admin=request.user,
                action=f"Created sector: {sector.sector.name}",
                action_type="sector_created",
                target_user=None,
            )

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('superadmin_dashboard')
                })
            return redirect('superadmin_dashboard')
        else:
            print("==== FORM IS INVALID ====")
            print("FORM ERRORS:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"- {field}: {error}")

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors.get_json_data()
                }, status=400)
            else:
                # Render form again with errors for non-AJAX POSTs
                return render(request, 'admin/create_sector.html', {'form': form})

    else:
        print("==== RECEIVED GET REQUEST ====")
        form = sectorCreateForm()

    return render(request, 'admin/create_sector.html', {'form': form})
