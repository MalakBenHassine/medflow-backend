from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']  # Supprimez 'role' des champs modifiables
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Attribuez un rôle par défaut
        validated_data['role'] = 'PATIENT'  # Rôle par défaut pour l'inscription
        password = validated_data.pop('password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            role=validated_data['role']
        )
        return user