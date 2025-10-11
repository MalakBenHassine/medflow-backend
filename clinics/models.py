# clinics/models.py
from django.db import models
from accounts.models import User, RoleEnum

class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)  # Ajouté pour complétude
    email = models.EmailField(blank=True)  # Ajouté
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    staff = models.ManyToManyField(User, related_name='clinics', limit_choices_to={'role__in': [RoleEnum.DOCTOR, RoleEnum.RECEPTIONIST, RoleEnum.ADMIN]})

    def add_staff(self, user):
        if user.role in [RoleEnum.DOCTOR, RoleEnum.RECEPTIONIST, RoleEnum.ADMIN]:
            self.staff.add(user)

class Service(models.Model):  # Nouveau modèle pour services avec tarifs
    id = models.AutoField(primary_key=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)