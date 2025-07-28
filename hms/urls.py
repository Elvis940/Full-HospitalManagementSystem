from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import dashboard_view  # Make sure to import your dashboard view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', dashboard_view, name='home'),  # This makes dashboard the home page
    path('billing/', include('billing.urls')),
    path('pharmacist/', include('pharmacy.urls')),
    path('doctor/', include('doctor.urls')),
    path('nurse/', include('nurse.urls')),
    path('receptionist/', include('receptionist.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)