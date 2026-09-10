from rest_framework import serializers
from .models import Clinic, Service
from accounts.serializers import UserSerializer

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'clinic', 'name', 'description', 'price', 'created_at', 'updated_at']

    def create(self, validated_data):
        clinic_id = validated_data.pop('clinic')
        service = Service.objects.create(clinic_id=clinic_id, **validated_data)
        return service

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

class ClinicSerializer(serializers.ModelSerializer):
    staff = UserSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'phone', 'email', 'staff', 'services', 'created_at', 'updated_at']

    def create(self, validated_data):
        staff_data = self.context.get('staff', [])
        clinic = Clinic.objects.create(**validated_data)
        for staff in staff_data:
            user_serializer = UserSerializer(data=staff)
            if user_serializer.is_valid():
                user = user_serializer.save()
                clinic.staff.add(user)
        return clinic

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance