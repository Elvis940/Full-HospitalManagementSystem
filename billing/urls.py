from django.urls import path
from . import views

urlpatterns = [
    path('generate-invoices/', views.generate_invoices, name='generate_invoices'),
    path('process-insurance-claims/', views.process_insurance_claims, name='process_insurance_claims'),
    path('manage-payment-plans/', views.manage_payment_plans, name='manage_payment_plans'),
    path('financial-reports/', views.financial_reports, name='financial_reports'),
    path('record-payments/', views.record_payments, name='record_payments'),
    
]
