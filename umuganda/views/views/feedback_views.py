from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from umuganda.models import Feedback
from users.models import UserProfile
from admn.models.cell_admin_membership import CellAdminMembership


@method_decorator(login_required, name='dispatch')
class UmugandaFeedbackListView(View):
    template_name = 'admin/feedback_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_level != 'cell_officer':
            messages.error(request, "Unauthorized access.")
            return redirect('admin_login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        admin = request.user

        try:
            membership = CellAdminMembership.objects.get(admin=admin)
            cell = membership.cell
        except CellAdminMembership.DoesNotExist:
            messages.error(request, "You are not assigned to any cell.")
            return render(request, 'admin/cell_not_assigned.html')

        # Filter feedback from users in this cell
        users_in_cell = UserProfile.objects.filter(cell=cell).values_list('user_id', flat=True)
        feedbacks = Feedback.objects.filter(user__id__in=users_in_cell).select_related('user', 'session', 'fine')

        context = {
            'feedbacks': feedbacks,
            'cell': cell,
        }
        return render(request, self.template_name, context)
