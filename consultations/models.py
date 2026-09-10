# consultations/models.py
from django.db import models
from appointments.models import Appointment

class DoctorProfile(models.Model):  
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'DOCTOR'})
    specialty = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Consultation(models.Model):
    id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='consultation')
    notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    tenant = models.ForeignKey('clinics.Clinic', null=True, blank=True, on_delete=models.SET_NULL, related_name='consultations')  # Pour multi-tenant
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_pdf(self):
        pass

class Prescription(models.Model):  
    id = models.AutoField(primary_key=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescriptions')
    medications = models.TextField()  
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_pdf(self):
        pass