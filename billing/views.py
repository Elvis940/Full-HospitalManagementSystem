from django.shortcuts import render

def generate_invoices(request):
    return render(request, 'billing/generate_invoices.html')

def process_insurance_claims(request):
    return render(request, 'billing/process_insurance_claims.html')

def manage_payment_plans(request):
    return render(request, 'billing/manage_payment_plans.html')

def financial_reports(request):
    return render(request, 'billing/financial_reports.html')

def record_payments(request):
    return render(request, 'billing/record_payments.html')