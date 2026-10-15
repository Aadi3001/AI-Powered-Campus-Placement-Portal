from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    """
    Public endpoint: anyone can POST here to create a new account.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    """GET -> basic details of the logged-in user, including their role."""

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
        })