from django.urls import path
from . import views

urlpatterns = [
    path('doctor-appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor-medical-reports/', views.doctor_medical_reports, name='doctor_medical_reports'),
    path('doctor-patients/', views.doctor_patients, name='doctor_patients'),
    path('doctor-prescription/', views.doctor_prescription, name='doctor_prescription'),
    path('doctor-schedule/', views.doctor_schedule, name='doctor_schedule'),
    
]
