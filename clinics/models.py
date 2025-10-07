from django.db import models
from accounts.models import User

class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    services = models.JSONField(default=list)  # Liste de services (ex: ['Consultation', 'Vaccin'])
    staff = models.ManyToManyField(User, related_name='clinics', limit_choices_to={'role__in': ['DOCTOR', 'RECEPTIONIST', 'ADMIN']})

    def add_staff(self, user):
        if user.role in ['DOCTOR', 'RECEPTIONIST', 'ADMIN']:
            self.staff.add(user)