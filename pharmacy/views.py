from django.shortcuts import render

def drug_interaction(request):
    return render(request, 'pharmacist/drug_interaction.html')

def manage_suppliers(request):
    return render(request, 'pharmacist/manage_suppliers.html')

def medication_inventory(request):
    return render(request, 'pharmacist/medication_inventory.html')

def pharmacy_reports(request):
    return render(request, 'pharmacist/pharmacy_reports.html')

def process_prescription(request):
    return render(request, 'pharmacist/process_prescription.html')