from django.db import models
from appointments.models import Appointment

class Consultation(models.Model):
    id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    prescription = models.JSONField(default=list)  

    def generate_pdf(self):
        pass