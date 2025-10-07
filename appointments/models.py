from django.db import models
from patients.models import PatientProfile
from accounts.models import User

class AppointmentStatusEnum(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    CONFIRMED = 'CONFIRMED', 'Confirmé'
    CANCELLED = 'CANCELLED', 'Annulé'
    COMPLETED = 'COMPLETED', 'Complété'

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'role': 'DOCTOR'})
    status = models.CharField(max_length=20, choices=AppointmentStatusEnum.choices, default='PENDING')

    def modify(self, new_date):
        self.date = new_date
        self.save()