from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from receptionist.models import Patient
from .forms import CustomUserCreationForm
from .models import User
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.role == 'ADMIN' or u.is_superuser)
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/manage_users.html', {'users': users})

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required
@user_passes_test(lambda u: u.role == 'ADMIN' or u.is_superuser)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        try:
            email_context = {
                'user': user,
                'admin': request.user,
                'protocol': 'https' if request.is_secure() else 'http',
                'domain': request.get_host()
            }
            
            if user.status == 'PENDING':
                # Activate account
                user.status = 'ACTIVE'
                user.is_active = True
                email_context['subject'] = "Your Account Has Been Activated"
                email_context['message'] = "Your account has been activated by the administrator. You can now log in to the system."
                success_msg = f"Activated user {user.username} and sent notification"
                
            elif user.status == 'ACTIVE':
                # Deactivate account
                user.status = 'DENIED'
                user.is_active = False
                email_context['subject'] = "Your Account Has Been Deactivated"
                email_context['message'] = "Your account has been deactivated by the administrator. Please contact support if you believe this is an error."
                success_msg = f"Deactivated user {user.username} and sent notification"
                
            else:
                messages.error(request, "Cannot modify a denied account")
                return redirect('manage_users')
            
            # Save user changes
            user.save()
            
            # Send email notification
            html_message = render_to_string('emails/account_status_update.html', email_context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=email_context['subject'],
                message=plain_message,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
            
            messages.success(request, success_msg)
            
        except Exception as e:
            messages.error(request, f"Error updating status: {str(e)}")
    
    return redirect('manage_users')

@login_required
@user_passes_test(lambda u: u.role == 'ADMIN' or u.is_superuser)
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'admin/view_user.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.role == 'ADMIN' or u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "You cannot edit superuser accounts!")
        return redirect('manage_users')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user.username} updated successfully!")
            return redirect('view_user', user_id=user.id)
    else:
        form = CustomUserCreationForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'admin/edit_user.html', context)

@login_required
@user_passes_test(lambda u: u.role == 'ADMIN' or u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.user == user:
        messages.error(request, "You cannot delete your own account!")
        return redirect('manage_users')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User {username} has been deleted successfully.")
        return redirect('manage_users')
    
    return render(request, 'admin/confirm_delete.html', {'user': user})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = 'PENDING'
            user.is_active = False
            user.save()
            
            messages.success(request, 'Registration successful! Your account is pending approval.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                if user.status == 'PENDING':
                    messages.error(request, 'Your account is pending approval. Please contact support if this is taking too long.')
                elif user.status == 'DENIED':
                    messages.error(request, 'Your account has been deactivated. Please contact support.')
                return redirect('login')
        except User.DoesNotExist:
            pass
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'DOCTOR':
                return redirect('doctor_dashboard')
            elif user.role == 'NURSE':
                return redirect('nurse_dashboard')
            elif user.role == 'RECEPTIONIST':
                return redirect('receptionist_dashboard')
            elif user.role == 'PHARMACIST':
                return redirect('pharmacist_dashboard')
            elif user.role == 'BILLING':
                return redirect('billing_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def accounts_home(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return redirect('login')

@login_required
def dashboard_view(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'DOCTOR':
        return redirect('doctor_dashboard')
    return render(request, 'accounts/dashboard.html')

@login_required
@user_passes_test(lambda u: u.role == 'ADMIN' or u.is_superuser)
def admin_dashboard(request):
    total_users = User.objects.count()
    pending_users = User.objects.filter(status='PENDING').count()
    active_users = User.objects.filter(status='ACTIVE').count()
    total_patients = Patient.objects.count()  # Add this line
    
    context = {
        'total_staff': total_users,
        'pending_users': pending_users,
        'active_users': active_users,
        'total_patients': total_patients,  # Add this line
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.role == 'DOCTOR')
def doctor_dashboard(request):
    return render(request, 'accounts/doctor_dashboard.html')

@login_required
@user_passes_test(lambda u: u.role == 'NURSE')
def nurse_dashboard(request):
    return render(request, 'accounts/nurse_dashboard.html')

@login_required
@user_passes_test(lambda u: u.role == 'RECEPTIONIST')
def receptionist_dashboard(request):
    total_patients = Patient.objects.count()
    context = {
        'total_patients': total_patients,
        # You can add other context variables here if needed
    }
    return render(request, 'accounts/receptionist_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.role == 'PHARMACIST')
def pharmacist_dashboard(request):
    return render(request, 'accounts/pharmacist_dashboard.html')

@login_required
@user_passes_test(lambda u: u.role == 'BILLING')
def billing_dashboard(request):
    return render(request, 'accounts/billing_dashboard.html')

def dashboard_view(request):
    # Get all users with role 'DOCTOR'
    doctors = User.objects.filter(role='DOCTOR')
    context = {
        'doctors': doctors
    }
    return render(request, 'accounts/dashboard.html', context)