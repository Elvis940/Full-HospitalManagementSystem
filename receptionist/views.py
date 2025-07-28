from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import PatientRegistrationForm, AppointmentForm,PatientEditForm
from .models import Patient, Appointment
from django.contrib.auth import get_user_model
import pandas as pd
from django.http import HttpResponse
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.http import JsonResponse
import json
from datetime import datetime


User = get_user_model()


# Calendar events endpoint
@login_required
def calendar_events(request):
    appointments = Appointment.objects.all()
    events = []
    
    for appointment in appointments:
        events.append({
            'id': appointment.id,
            'title': f"{appointment.patient.full_name} - Dr. {appointment.doctor.last_name}",
            'start': f"{appointment.date}T{appointment.start_time}",
            'end': f"{appointment.date}T{appointment.end_time}",
            'color': '#28a745' if appointment.status == 'CONFIRMED' else 
                    '#dc3545' if appointment.status == 'CANCELLED' else 
                    '#007bff',
            'extendedProps': {
                'patient': appointment.patient.full_name,
                'doctor': f"Dr. {appointment.doctor.get_full_name()}",
                'status': appointment.get_status_display(),
                'notes': appointment.notes or ""
            }
        })
    return JsonResponse(events, safe=False)

@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('receptionist_appointments')
    
    return render(request, 'receptionist/confirm_appointment_delete.html', {'appointment': appointment})

@login_required
def confirm_delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'receptionist/confirm_appointment_delete.html', {'appointment': appointment})



@login_required
def confirm_cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.status == 'CANCELLED':
        messages.warning(request, 'This appointment is already cancelled')
        return redirect('receptionist_appointments')
    return render(request, 'receptionist/confirm_cancel_appointment.html', {'appointment': appointment})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        try:
            appointment.status = 'CANCELLED'
            appointment.cancel_reason = request.POST.get('reason', 'No reason provided')
            appointment.save()
            
            # Send WebSocket notification after successful cancellation
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "appointments",
                {
                    "type": "appointment.update",
                    "message": f"Appointment {appointment.id} cancelled",
                    "appointment_id": appointment.id,
                    "status": "CANCELLED"
                }
            )
            
            messages.success(request, 'Appointment cancelled successfully!')
            return redirect('receptionist_appointments')
            
        except Exception as e:
            messages.error(request, f'Error cancelling appointment: {str(e)}')
            return redirect('receptionist_appointments')
    
    # If not POST, redirect to confirmation page
    return redirect('confirm_cancel_appointment', appointment_id=appointment_id)

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            
            # Send WebSocket notification after successful update
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "appointments",
                {
                    "type": "appointment.update",
                    "message": f"Appointment {appointment.id} updated",
                    "appointment_id": appointment.id,
                    "status": appointment.status
                }
            )
            
            messages.success(request, 'Appointment updated successfully!')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment updated successfully!',
                    'appointment_id': appointment.id
                })
            return redirect('receptionist_appointments')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors.get_json_data()
                }, status=400)
    
    # GET request handling
    context = {
        'form': AppointmentForm(instance=appointment),
        'appointment': appointment,
        'patients': Patient.objects.all(),
        'doctors': User.objects.filter(role='DOCTOR', is_active=True)
    }
    return render(request, 'receptionist/edit_appointment.html', context)
     
@login_required
def view_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'receptionist/view_appointment.html', {'appointment': appointment})

@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            
            # Send WebSocket notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "appointments",
                {
                    "type": "appointment.update",
                    "message": f"New appointment {appointment.id} created",
                    "appointment_id": appointment.id,
                    "status": appointment.status
                }
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment scheduled successfully!',
                    'appointment': {
                        'id': appointment.id,
                        'patient': appointment.patient.full_name,
                        'doctor': appointment.doctor.get_full_name(),
                        'date': appointment.date.strftime('%Y-%m-%d'),
                        'start_time': appointment.start_time.strftime('%H:%M'),
                        'end_time': appointment.end_time.strftime('%H:%M'),
                        'notes': appointment.notes or "-",
                    },
                    'event': {
                        'id': appointment.id,
                        'title': f"{appointment.patient.full_name} - Dr. {appointment.doctor.last_name}",
                        'start': f"{appointment.date}T{appointment.start_time}",
                        'end': f"{appointment.date}T{appointment.end_time}",
                        'color': '#28a745',
                        'extendedProps': {
                            'patient': appointment.patient.full_name,
                            'doctor': f"Dr. {appointment.doctor.get_full_name()}",
                            'status': appointment.status,
                            'notes': appointment.notes or ""
                        }
                    }
                })
            
            messages.success(request, 'Appointment scheduled successfully!')
            return redirect('receptionist_appointments')
    
    # GET request handling
    today = timezone.now().date()
    appointments = Appointment.objects.all().select_related('patient', 'doctor').order_by('date', 'start_time')
    
    context = {
        'patients': Patient.objects.all(),
        'doctors': User.objects.filter(role='DOCTOR', is_active=True),
        'todays_appointments': appointments,
        'today': today,
        'showing_all': True,
    }
    return render(request, 'receptionist/receptionist_appointments.html', context)

@login_required
def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient registered successfully!')
            return redirect('patient_registration')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'receptionist/patient_registration.html', {'form': form})

@login_required
def patient_management(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        patients = Patient.objects.filter(
            Q(full_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query)
        ).order_by('full_name')
    else:
        patients = Patient.objects.all().order_by('full_name')
    
    if request.GET.get('export') == 'excel':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="patients.xlsx"'
        
        data = []
        for patient in patients:
            data.append([
                patient.full_name,
                patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else '',
                patient.gender,
                patient.phone_number,
                patient.email,
                patient.insurance_provider,
                patient.policy_number,
            ])
        
        df = pd.DataFrame(data, columns=[
            'Full Name', 'Date of Birth', 'Gender', 'Phone Number', 
            'Email', 'Insurance Provider', 'Policy Number'
        ])
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Patients')
        
        return response
    
    context = {
        'patients': patients,
        'patient_count': patients.count(),
        'search_query': search_query,
    }
    return render(request, 'receptionist/patient_management.html', context)

@login_required
def view_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'receptionist/view_patient.html', {'patient': patient})

@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PatientEditForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('patient_management')
    else:
        form = PatientEditForm(instance=patient)
    
    return render(request, 'receptionist/edit_patient.html', {'form': form, 'patient': patient})

@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
        return redirect('patient_management')
    
    return render(request, 'receptionist/confirm_delete.html', {'patient': patient})

def receptionist_appointments(request):
    return render(request, 'receptionist/receptionist_appointments.html')

def walk_in_management(request):
    return render(request, 'receptionist/walk_in_management.html')

def patient_checkin(request):
    return render(request, 'receptionist/patient_checkin.html')

def billing_coordination(request):
    return render(request, 'receptionist/billing_coordination.html')