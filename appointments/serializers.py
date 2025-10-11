# appointments/serializers.py
from rest_framework import serializers
from .models import Appointment, AppointmentStatusEnum
from accounts.serializers import UserSerializer
from patients.serializers import PatientProfileSerializer
from clinics.serializers import ServiceSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer()
    doctor = UserSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'patient', 'doctor', 'service', 'reason', 'status', 'tenant', 'created_at', 'updated_at']
        extra_kwargs = {'status': {'default': AppointmentStatusEnum.PENDING}}

    def create(self, validated_data):
        patient_data = validated_data.pop('patient')
        doctor_data = validated_data.pop('doctor')
        service_data = validated_data.pop('service', None)
        
        patient_serializer = PatientProfileSerializer(data=patient_data)
        doctor_serializer = UserSerializer(data=doctor_data)
        service_serializer = ServiceSerializer(data=service_data) if service_data else None

        if patient_serializer.is_valid() and doctor_serializer.is_valid() and (not service_data or service_serializer.is_valid()):
            patient = patient_serializer.save()
            doctor = doctor_serializer.save(role=RoleEnum.DOCTOR)
            service = service_serializer.save() if service_serializer else None
            appointment = Appointment.objects.create(
                patient=patient.user,
                doctor=doctor,
                service=service,
                date=validated_data['date'],
                status=validated_data.get('status', AppointmentStatusEnum.PENDING),
                tenant=validated_data.get('tenant')
            )
            return appointment
        raise serializers.ValidationError({
            'patient': patient_serializer.errors,
            'doctor': doctor_serializer.errors,
            'service': service_serializer.errors if service_serializer else {}
        })

    def update(self, instance, validated_data):
        patient_data = validated_data.pop('patient', None)
        doctor_data = validated_data.pop('doctor', None)
        service_data = validated_data.pop('service', None)

        if patient_data:
            patient_serializer = PatientProfileSerializer(instance.patient, data=patient_data, partial=True)
            if patient_serializer.is_valid():
                patient_serializer.save()
        if doctor_data:
            doctor_serializer = UserSerializer(instance.doctor, data=doctor_data, partial=True)
            if doctor_serializer.is_valid():
                doctor_serializer.save()
        if service_data:
            service_serializer = ServiceSerializer(instance.service, data=service_data, partial=True)
            if service_serializer.is_valid():
                service_serializer.save()

        instance.date = validated_data.get('date', instance.date)
        instance.status = validated_data.get('status', instance.status)
        instance.tenant = validated_data.get('tenant', instance.tenant)
        instance.save()
        return instance