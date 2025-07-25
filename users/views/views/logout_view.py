from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

from umuganda.utils.logging import log_admin_action  
class LogoutView(View):
    def get(self, request):
        user = request.user

        # ✅ Log the logout action before the session ends
        if user.is_authenticated and (user.user_level.startswith('admin_') or user.user_level == 'super_admin'):
            log_admin_action(
                admin=user,
                action="Admin logged out",
                action_type="logout"
            )

        logout(request)
        return redirect('admin_login')  # Adjust this if needed
