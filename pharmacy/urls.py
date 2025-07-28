from django.urls import path
from . import views

urlpatterns = [
    path('drug-interaction/', views.drug_interaction, name='drug_interaction'),
    path('manage-suppliers/', views.manage_suppliers, name='manage_suppliers'),
    path('medication-inventory/', views.medication_inventory, name='medication_inventory'),
    path('pharmacy-reports/', views.pharmacy_reports, name='pharmacy_reports'),
    path('process-prescription/', views.process_prescription, name='process_prescription'),
    
]
