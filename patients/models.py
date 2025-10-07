from django.db import models
from accounts.models import User

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'PATIENT'})
    contact_info = models.CharField(max_length=255)
    medical_history = models.TextField(blank=True)
    update_profile = models.BooleanField(default=False)  