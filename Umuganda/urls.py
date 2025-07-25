from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from users.views.views.adresses import get_cells, get_districts, get_sectors, get_villages
from users.views.views.get_cells import get_cells_by_logged_in_sector

from django.shortcuts import render

def home(request):
    return render(request, 'admin/home.html')


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/citizens/', include('users.urls')),

    path('ajax/get-districts/', get_districts, name='get_districts'),
    path('ajax/get-sectors/', get_sectors, name='get_sectors'),
    path('ajax/get-cells/', get_cells, name='get_cells'),
    path('ajax/get-villages/', get_villages, name='get_villages'),
    path('ajax/get-cells-by-sector/', get_cells_by_logged_in_sector, name='get_cells_by_logged_in_sector'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
