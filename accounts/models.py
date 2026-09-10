# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class RoleEnum(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    DOCTOR = 'DOCTOR', 'Médecin'
    RECEPTIONIST = 'RECEPTIONIST', 'Réceptionniste'
    PATIENT = 'PATIENT', 'Patient'

class CustomUserManager(BaseUserManager):  # Changez models.Manager en BaseUserManager
    def create_user(self, email, password, role, **extra_fields):
        if not email:
            raise ValueError(_('L\'email doit être défini'))
        email = self.normalize_email(email)  # Maintenant disponible grâce à BaseUserManager
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, role, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_superuser=True.'))
        return self.create_user(email, password, role, **extra_fields)

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=RoleEnum.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant = models.ForeignKey('clinics.Clinic', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')

    # Supprimez username des champs requis
    username = None  # Désactive l'utilisation de username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']  # Ajoute role comme champ requis

    objects = CustomUserManager()  # Utilisez le gestionnaire personnalisé

    # Related_names uniques pour groups/permissions (bien, conservé)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='medflow_users_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='medflow_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()

    class Meta:
        db_table = 'users'