from rest_framework import generics, permissions
from .models import (Company, RecruiterProfile)
from .serializers import (CompanySerializer, RecruiterProfileSerializer)


class CompanyListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list all companies (any authenticated user can see them)
    POST -> create a new company (any authenticated user can add one)
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class MyRecruiterProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  -> returns the logged-in recruiter's own profile
    PUT/PATCH -> updates the logged-in recruiter's own profile
    """
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.recruiter_profile