# accounts/urls.py
from django.urls import path
from .views import RegisterView, CustomLoginView ,AssignRoleView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('assign-role/<int:user_id>/', AssignRoleView.as_view(), name='assign_role'),
]