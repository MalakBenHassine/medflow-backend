# patients/models.py
from django.db import models
from accounts.models import User

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'PATIENT'})
    contact_info = models.CharField(max_length=255)  # ex. téléphone
    birth_date = models.DateField(null=True, blank=True)  # Ajouté pour contexte médical
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], blank=True)  # Ajouté
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)