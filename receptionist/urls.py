from django.urls import path
from . import views

urlpatterns = [
    # Patient-related URLs
    path('register-patient/', views.patient_registration, name='patient_registration'),
    path('patient-management/', views.patient_management, name='patient_management'),
    path('patients/<int:patient_id>/', views.view_patient, name='view_patient'),
    path('patients/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),

    # Appointment-related URLs
    path('appointments/', views.schedule_appointment, name='receptionist_appointments'),
    path('appointments/<int:appointment_id>/view/', views.view_appointment, name='view_appointment'),
    path('appointments/<int:appointment_id>/edit/', views.edit_appointment, name='edit_appointment'),
    
    # Appointment cancellation flow (2-step process)
    path('appointments/<int:appointment_id>/cancel/', views.confirm_cancel_appointment, name='confirm_cancel_appointment'),
    path('appointments/<int:appointment_id>/cancel/confirm/', views.cancel_appointment, name='cancel_appointment'),
    
    # Appointment deletion flow (2-step process)
    path('appointments/<int:appointment_id>/delete/', views.confirm_delete_appointment, name='confirm_delete_appointment'),
    path('appointments/<int:appointment_id>/delete/confirm/', views.delete_appointment, name='delete_appointment'),
    
    #real time calender 
    path('appointments/calendar-events/', views.calendar_events, name='calendar_events'),

    # Other receptionist URLs
    path('walk-in/', views.walk_in_management, name='walk_in_management'),
    path('check-in/', views.patient_checkin, name='patient_checkin'),
    path('billing/', views.billing_coordination, name='billing_coordination'),
    
    
]