# appointments/models.py
from django.db import models
from accounts.models import User

class AppointmentStatusEnum(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    CONFIRMED = 'CONFIRMED', 'Confirmé'
    CANCELLED = 'CANCELLED', 'Annulé'
    COMPLETED = 'COMPLETED', 'Complété'

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    patient = models.ForeignKey('patients.PatientProfile', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'role': 'DOCTOR'})
    service = models.ForeignKey('clinics.Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')  # Ajouté lien vers service
    reason = models.TextField(blank=True)  # Ajouté pour contexte
    status = models.CharField(max_length=20, choices=AppointmentStatusEnum.choices, default='PENDING')
    tenant = models.ForeignKey('clinics.Clinic', null=True, blank=True, on_delete=models.SET_NULL, related_name='appointments')  # Pour multi-tenant
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def modify(self, new_date):
        self.date = new_date
        self.save()