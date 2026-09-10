from rest_framework import serializers
from .models import Invoice, Payment, PaymentStatusEnum
from patients.serializers import PatientProfileSerializer
from appointments.serializers import AppointmentSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer()
    appointment = AppointmentSerializer()

    class Meta:
        model = Invoice
        fields = ['id', 'patient', 'appointment', 'amount', 'status', 'tenant', 'created_at', 'updated_at']
        extra_kwargs = {'status': {'default': PaymentStatusEnum.PENDING}}

    def create(self, validated_data):
        patient_data = validated_data.pop('patient')
        appointment_data = validated_data.pop('appointment', None)
        
        patient_serializer = PatientProfileSerializer(data=patient_data)
        appointment_serializer = AppointmentSerializer(data=appointment_data) if appointment_data else None

        if patient_serializer.is_valid() and (not appointment_data or appointment_serializer.is_valid()):
            patient = patient_serializer.save()
            appointment = appointment_serializer.save() if appointment_serializer else None
            invoice = Invoice.objects.create(
                patient=patient.user,
                appointment=appointment,
                amount=validated_data['amount'],
                status=validated_data.get('status', PaymentStatusEnum.PENDING),
                tenant=validated_data.get('tenant')
            )
            return invoice
        raise serializers.ValidationError({
            'patient': patient_serializer.errors,
            'appointment': appointment_serializer.errors if appointment_serializer else {}
        })

    def update(self, instance, validated_data):
        patient_data = validated_data.pop('patient', None)
        appointment_data = validated_data.pop('appointment', None)

        if patient_data:
            patient_serializer = PatientProfileSerializer(instance.patient, data=patient_data, partial=True)
            if patient_serializer.is_valid():
                patient_serializer.save()
        if appointment_data:
            appointment_serializer = AppointmentSerializer(instance.appointment, data=appointment_data, partial=True)
            if appointment_serializer.is_valid():
                appointment_serializer.save()

        instance.amount = validated_data.get('amount', instance.amount)
        instance.status = validated_data.get('status', instance.status)
        instance.tenant = validated_data.get('tenant', instance.tenant)
        instance.save()
        return instance

class PaymentSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'amount', 'payment_method', 'transaction_id', 'created_at', 'updated_at']
        extra_kwargs = {'payment_method': {'default': 'Stripe'}}

    def create(self, validated_data):
        invoice_data = validated_data.pop('invoice')
        invoice_serializer = InvoiceSerializer(data=invoice_data)
        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            payment = Payment.objects.create(
                invoice=invoice,
                amount=validated_data['amount'],
                payment_method=validated_data.get('payment_method', 'Stripe'),
                transaction_id=validated_data.get('transaction_id', '')
            )
            return payment
        raise serializers.ValidationError(invoice_serializer.errors)

    def update(self, instance, validated_data):
        invoice_data = validated_data.pop('invoice', None)
        if invoice_data:
            invoice_serializer = InvoiceSerializer(instance.invoice, data=invoice_data, partial=True)
            if invoice_serializer.is_valid():
                invoice_serializer.save()
        instance.amount = validated_data.get('amount', instance.amount)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.transaction_id = validated_data.get('transaction_id', instance.transaction_id)
        instance.save()
        return instance