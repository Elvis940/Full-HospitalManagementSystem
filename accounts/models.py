from django.contrib.auth.models import AbstractUser
from django.db import models
import cloudinary.models

class User(AbstractUser):
    # Role Choices
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('RECEPTIONIST', 'Receptionist'),
        ('PHARMACIST', 'Pharmacist'),
        ('BILLING', 'Billing Staff'),
    )
    
    # Status Choices
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('DENIED', 'Denied'),
    )
    
    # Fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    profile_picture = cloudinary.models.CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        """Ensure is_active matches status"""
        self.is_active = (self.status == 'ACTIVE')
        super().save(*args, **kwargs)
    
    def get_status_display(self):
        """Custom status display that considers both status and is_active"""
        if self.status == 'DENIED':
            return 'Denied'
        return 'Active' if self.is_active else 'Pending'
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        If first_name and last_name are not available, return username.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"