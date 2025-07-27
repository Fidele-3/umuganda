from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from umuganda.models import UmugandaSession, CellUmugandaSession
from umuganda.forms.umuganda_seesion_form import UmugandaSessionForm


@method_decorator(login_required, name='dispatch')
class UmugandaSessionDetailView(View):
    def get(self, request, session_id):
        user = request.user

        # ✅ Sector officer: can directly access UmugandaSession
        if user.user_level == 'sector_officer':
            session = get_object_or_404(UmugandaSession, pk=session_id)
            form = UmugandaSessionForm(instance=session)
            cell_sessions = CellUmugandaSession.objects.filter(sector_session=session)

            return render(request, 'admin/session_detail.html', {
                'session': session,
                'form': form,
                'can_edit': True,
                'cell_sessions': cell_sessions,
                'cell_session': None,  # ✅ Added
            })


        # ✅ Cell officer: should only access their own CellUmugandaSession
        elif user.user_level == 'cell_officer':
            try:
                cell_session = CellUmugandaSession.objects.get(
                    pk=session_id,
                    updated_by=user  # Adjust this if you're using a different link (e.g. admin)
                )
            except CellUmugandaSession.DoesNotExist:
                return render(request, 'admin/cell_not_assigned.html')

            return render(request, 'admin/session_detail.html', {
                'session': cell_session.sector_session,  # This is the sector-level session
                'cell_session': cell_session,            # ✅ Add this line
                'form': None,
                'can_edit': True,
                'cell_sessions': [cell_session],
            })

        # 🚫 Not authorized
        return render(request, 'admin/cell_not_assigned.html')

    def post(self, request, session_id):
        user = request.user

        if user.user_level != 'sector_officer':
            return render(request, 'admin/cell_not_assigned.html')

        session = get_object_or_404(UmugandaSession, pk=session_id)
        form = UmugandaSessionForm(request.POST, instance=session)

        if form.is_valid():
            updated_session = form.save(commit=False)
            updated_session.updated_by = user
            updated_session.save()
            messages.success(request, "Sector-level Umuganda session updated successfully.")
            return redirect('umuganda_session_detail', session_id=session_id)

        return render(request, 'admin/session_detail.html', {
            'session': session,
            'form': form,
            'can_edit': True,
        })
