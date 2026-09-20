from rest_framework import generics, permissions
from .models import (Company, RecruiterProfile, SkillTag, Job)
from .serializers import (CompanySerializer, RecruiterProfileSerializer, SkillTagSerializer, JobSerializer)


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


class SkillTagListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list all skill tags (shared master list)
    POST -> add a new skill tag
    """
    queryset = SkillTag.objects.all()
    serializer_class = SkillTagSerializer
    permission_classes = [permissions.IsAuthenticated]


class JobListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list all jobs (visible to everyone — students need to browse them)
    POST -> create a new job, automatically owned by the logged-in recruiter
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user.recruiter_profile)