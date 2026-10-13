from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from recruiters.models import Job
from .predict import predict_selection_probability


class MyChanceView(APIView):
    """
    GET -> the logged-in student's estimated chance of selection for a job.
    No estimate is given if the student is not eligible or has no CGPA.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_id):
        if request.user.role != 'STUDENT':
            return Response(
                {"detail": "Only students can request a selection estimate."},
                status=status.HTTP_403_FORBIDDEN,
            )

        job = get_object_or_404(Job, pk=job_id)

        try:
            result = predict_selection_probability(request.user.student_profile, job)
        except FileNotFoundError:
            return Response(
                {"detail": "The prediction model has not been trained yet."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(result)