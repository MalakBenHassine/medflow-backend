# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from .models import User, RoleEnum

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Autorise l'inscription sans authentification

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(email=request.data['email'])
            response.data['user'] = {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'tenant': user.tenant_id if user.tenant else None,
            }
        return response
    

class AssignRoleView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Seuls les admins peuvent accéder

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        role = request.data.get('role')
        # Utilisez RoleEnum.choices directement
        valid_roles = dict(RoleEnum.choices).keys()  # Récupère les valeurs possibles
        if role in valid_roles and role != 'PATIENT':
            user.role = role
            user.save()
            return Response({"message": f"Role updated to {role}"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid or unauthorized role"}, status=status.HTTP_400_BAD_REQUEST)