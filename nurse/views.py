from django.shortcuts import render

def medication_management(request):
    return render(request, 'nurse/medication_management.html')

def nurse_procedure_assistance(request):
    return render(request, 'nurse/nurse_procedure_assistance.html')

def nurse_reports(request):
    return render(request, 'nurse/nurse_reports.html')

def patient_records(request):
    return render(request, 'nurse/patient_records.html')

def update_vitals(request):
    return render(request, 'nurse/update_vitals.html')