from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleEnum(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    DOCTOR = 'DOCTOR', 'Médecin'
    RECEPTIONIST = 'RECEPTIONIST', 'Réceptionniste'
    PATIENT = 'PATIENT', 'Patient'

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hashé auto par Django
    role = models.CharField(max_length=20, choices=RoleEnum.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    tenant_id = models.IntegerField(null=True, blank=True)  # Pour multi-tenant

    # Ajoute des related_name uniques
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='medflow_users_groups',  # Nom unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='medflow_users_permissions',  # Nom unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()

    class Meta:
        db_table = 'users'