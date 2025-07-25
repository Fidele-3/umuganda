from django.shortcuts import render, redirect
from admn.forms.super_admin_register import SuperAdminRegistrationForm
from django.contrib import messages

def super_admin_register_view(request):
    if request.method == 'POST':
        form = SuperAdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Super Admin account created. You can now log in.")
            return redirect('admin_login')  # Replace with your login URL name
    else:
        form = SuperAdminRegistrationForm()
    return render(request, 'admin/admin_register.html', {'form': form})
