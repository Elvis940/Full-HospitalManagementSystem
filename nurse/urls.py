from django.urls import path
from . import views

urlpatterns = [
    path('medication-management/', views.medication_management, name='medication_management'),
    path('nurse-procedure-assistance/', views.nurse_procedure_assistance, name='nurse_procedure_assistance'),
    path('nurse-reports/', views.nurse_reports, name='nurse_reports'),
    path('patients-records/', views.patient_records, name='patient_records'),
    path('update-vitals/', views.update_vitals, name='update_vitals'),
    
]
