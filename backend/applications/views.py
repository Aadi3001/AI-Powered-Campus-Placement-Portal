from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Application
from .serializers import ApplicationSerializer, ApplicationStatusUpdateSerializer


class MyApplicationsView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(student=self.request.user.student_profile)

    def perform_create(self, serializer):
        student = self.request.user.student_profile
        job = serializer.validated_data['job']
        if Application.objects.filter(student=student, job=job).exists():
            raise ValidationError("You have already applied to this job.")
        serializer.save(student=student)
        

class JobApplicantsView(generics.ListAPIView):
    """
    GET -> list all applications for a specific job,
    but only if the logged-in recruiter owns that job.
    """
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Application.objects.filter(
            job_id=job_id,
            job__recruiter=self.request.user.recruiter_profile,
        )


class UpdateApplicationStatusView(generics.UpdateAPIView):
    """
    PATCH -> update the status of an application,
    but only if the logged-in recruiter owns the related job.
    """
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            job__recruiter=self.request.user.recruiter_profile
        )