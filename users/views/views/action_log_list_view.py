# admin/views/action_log_list_view.py

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from admn.models import AdminActionLog

class AdminActionLogListView(LoginRequiredMixin, ListView):
    model = AdminActionLog
    template_name = 'admin/action_log_list.html'
    context_object_name = 'logs'
    paginate_by = 25

    def get_queryset(self):
        return AdminActionLog.objects.select_related('admin', 'target_user').order_by('-timestamp')
