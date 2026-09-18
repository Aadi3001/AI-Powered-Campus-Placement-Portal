from rest_framework import generics, permissions
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Public endpoint: anyone can POST here to create a new account.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]