from django.db import migrations
from datetime import date

def fix_dates(apps, schema_editor):
    Appointment = apps.get_model('receptionist', 'Appointment')
    # Set default date for any NULL values
    Appointment.objects.filter(date__isnull=True).update(date=date(2025, 7, 1))
    
    # Convert any existing dates to proper format
    for app in Appointment.objects.all():
        if app.date.year < 2025:  # Check for invalid dates
            app.date = date(2025, 7, 1)
            app.save()

class Migration(migrations.Migration):
    
    dependencies = [
        # This MUST match your last migration file name exactly
        ('receptionist', '0002_appointment'),  
    ]

    operations = [
        migrations.RunPython(fix_dates),
    ]