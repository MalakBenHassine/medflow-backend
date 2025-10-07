from django.db import models
from patients.models import PatientProfile
from appointments.models import Appointment

class PaymentStatusEnum(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    PAID = 'PAID', 'Payé'
    OVERDUE = 'OVERDUE', 'En retard'

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='invoices')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatusEnum.choices, default='PENDING')

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255, default='Stripe')  # Intégration test mode
    transaction_id = models.CharField(max_length=255, blank=True)