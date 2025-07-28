from django.contrib import admin
from .models import Patient, Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'start_time', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = (
        'patient__full_name', 
        'doctor__first_name', 
        'doctor__last_name'
    )
    date_hierarchy = 'date'