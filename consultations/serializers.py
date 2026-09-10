from rest_framework import serializers
from .models import Consultation, DoctorProfile, Prescription
from appointments.serializers import AppointmentSerializer

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DoctorProfile
        fields = ['user', 'specialty', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(role=RoleEnum.DOCTOR)
            doctor_profile = DoctorProfile.objects.create(user=user, **validated_data)
            return doctor_profile
        raise serializers.ValidationError(user_serializer.errors)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        instance.specialty = validated_data.get('specialty', instance.specialty)
        instance.save()
        return instance

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'consultation', 'medications', 'instructions', 'created_at', 'updated_at']

    def create(self, validated_data):
        consultation_id = validated_data.pop('consultation')
        prescription = Prescription.objects.create(consultation_id=consultation_id, **validated_data)
        return prescription

    def update(self, instance, validated_data):
        instance.medications = validated_data.get('medications', instance.medications)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.save()
        return instance

class ConsultationSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer()
    prescriptions = PrescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'appointment', 'notes', 'diagnosis', 'prescriptions', 'tenant', 'created_at', 'updated_at']

    def create(self, validated_data):
        appointment_data = validated_data.pop('appointment')
        appointment_serializer = AppointmentSerializer(data=appointment_data)
        if appointment_serializer.is_valid():
            appointment = appointment_serializer.save()
            consultation = Consultation.objects.create(
                appointment=appointment,
                notes=validated_data.get('notes', ''),
                diagnosis=validated_data.get('diagnosis', ''),
                tenant=validated_data.get('tenant')
            )
            return consultation
        raise serializers.ValidationError(appointment_serializer.errors)

    def update(self, instance, validated_data):
        appointment_data = validated_data.pop('appointment', None)
        if appointment_data:
            appointment_serializer = AppointmentSerializer(instance.appointment, data=appointment_data, partial=True)
            if appointment_serializer.is_valid():
                appointment_serializer.save()
        instance.notes = validated_data.get('notes', instance.notes)
        instance.diagnosis = validated_data.get('diagnosis', instance.diagnosis)
        instance.tenant = validated_data.get('tenant', instance.tenant)
        instance.save()
        return instance