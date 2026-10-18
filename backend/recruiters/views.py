from rest_framework import generics, permissions
from students.utils import extract_skills_from_text
from .models import (Company, RecruiterProfile, SkillTag, Job)
from .serializers import (CompanySerializer, RecruiterProfileSerializer, SkillTagSerializer, JobSerializer, RecruiterJobSerializer)
from django.db.models import Count
from accounts.permissions import IsRecruiter, IsRecruiterOrReadOnly


class CompanyListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list all companies (any authenticated user can see them)
    POST -> create a new company (any authenticated user can add one)
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsRecruiterOrReadOnly]


class MyRecruiterProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  -> returns the logged-in recruiter's own profile
    PUT/PATCH -> updates the logged-in recruiter's own profile
    """
    serializer_class = RecruiterProfileSerializer
    permission_classes = [IsRecruiter]

    def get_object(self):
        return self.request.user.recruiter_profile


class SkillTagListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list all skill tags (shared master list)
    POST -> add a new skill tag
    """
    queryset = SkillTag.objects.all()
    serializer_class = SkillTagSerializer
    permission_classes = [IsRecruiterOrReadOnly]


class JobListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list all jobs (visible to everyone — students need to browse them)
    POST -> create a new job, automatically owned by the logged-in recruiter.
            If no required_skills were specified, auto-detect them from
            the job description using the same NLP technique as resumes.
    """
    queryset = Job.objects.prefetch_related('required_skills')
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOrReadOnly]
    
    def perform_create(self, serializer):
        job = serializer.save(recruiter=self.request.user.recruiter_profile)

        if not job.required_skills.exists():
            all_skill_names = list(SkillTag.objects.values_list('name', flat=True))
            found_skill_names = extract_skills_from_text(job.description, all_skill_names)

            matching_tags = SkillTag.objects.filter(name__in=found_skill_names)
            job.required_skills.set(matching_tags)


class MyJobsView(generics.ListAPIView):
    """GET -> the logged-in recruiter's own jobs, with applicant counts."""
    serializer_class = RecruiterJobSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        return (
            Job.objects.filter(recruiter=self.request.user.recruiter_profile)
            .prefetch_related('required_skills')
            .annotate(applicant_count=Count('applications'))
            .order_by('-created_at')
        )