from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import manage_users, toggle_user_status, view_user, edit_user, delete_user, login_view, logout_view, register_view, dashboard_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    path('admin/users/', manage_users, name='manage_users'),
    path('admin/users/<int:user_id>/toggle-status/', toggle_user_status, name='toggle_user_status'),
    path('admin/users/<int:user_id>/view/', view_user, name='view_user'),
    path('admin/users/<int:user_id>/edit/', edit_user, name='edit_user'),
    path('admin/users/<int:user_id>/delete/', delete_user, name='delete_user'),
    
    
    # Dashboard URLs
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('nurse/dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
    path('receptionist/dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('pharmacist/dashboard/', views.pharmacist_dashboard, name='pharmacist_dashboard'),
    path('billing/dashboard/', views.billing_dashboard, name='billing_dashboard'),

    # Add other URLs for each role's functionality
    
    # Password reset URLs
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

]