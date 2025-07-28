from django.shortcuts import render

def doctor_appointments(request):
    return render(request, 'doctor/doctor_appointments.html')

def doctor_medical_reports(request):
    return render(request, 'doctor/doctor_medical_reports.html')

def doctor_patients(request):
    return render(request, 'doctor/doctor_patients.html')

def doctor_prescription(request):
    return render(request, 'doctor/doctor_prescription.html')

def doctor_schedule(request):
    return render(request, 'doctor/doctor_schedule.html')