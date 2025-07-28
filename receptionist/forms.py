# receptionist/forms.py
from django import forms
from .models import Patient, Appointment
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'full_name', 
            'date_of_birth', 
            'gender',
            'phone_number', 
            'email',
            'insurance_provider', 
            'policy_number'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'insurance_provider': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(role='DOCTOR', status='ACTIVE')
        self.fields['date'].widget.attrs['min'] = timezone.now().date()
        self.fields['start_time'].widget.attrs['step'] = 900
        self.fields['end_time'].widget.attrs['step'] = 900
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'start_time', 'end_time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }