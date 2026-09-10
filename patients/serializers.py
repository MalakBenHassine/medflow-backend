# patients/serializers.py
from rest_framework import serializers
from .models import PatientProfile
from accounts.serializers import UserSerializer

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PatientProfile
        fields = ['user', 'contact_info', 'birth_date', 'gender', 'medical_history', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(role=RoleEnum.PATIENT)
            patient_profile = PatientProfile.objects.create(user=user, **validated_data)
            return patient_profile
        raise serializers.ValidationError(user_serializer.errors)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        instance.contact_info = validated_data.get('contact_info', instance.contact_info)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.medical_history = validated_data.get('medical_history', instance.medical_history)
        instance.save()
        return instance