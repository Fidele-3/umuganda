from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import CustomUser
from umuganda.utils.logging import log_admin_action  # <-- Import your logging function

def admin_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # ✅ Check if user is allowed (admin levels)
            if user.user_level in ['super_admin', 'sector_officer', 'cell_officer']:
                login(request, user)

                # ✅ Log the login action
                log_admin_action(
                    admin=user,
                    action="Admin logged in",
                    action_type="login"
                )

                # ✅ Redirect based on level
                if user.user_level == 'super_admin':
                    return redirect('superadmin_dashboard')
                elif user.user_level == 'sector_officer':
                    return redirect('sector_officer_dashboard')
                elif user.user_level == 'cell_officer':
                    return redirect('cell_officer_dashboard')
            else:
                messages.error(request, 'Only admins can log in here.')
                return redirect('admin_login')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('admin_login')

    return render(request, 'admin/login.html')
