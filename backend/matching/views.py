from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from recruiters.models import Job
from applications.models import Application
from .utils import generate_match_report
from django.shortcuts import get_object_or_404
from .recommendations import recommend_skills
from accounts.permissions import IsRecruiter


class JobMatchReportView(APIView):
    """
    GET -> for a given job, returns a ranked match report for every
    student who has applied, but only if the logged-in recruiter
    owns that job.
    """
    permission_classes = [IsRecruiter]

    def get(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id, recruiter=request.user.recruiter_profile)
        except Job.DoesNotExist:
            return Response(
                {"detail": "Job not found or you do not own this job."},
                status=status.HTTP_404_NOT_FOUND,
            )

        applications = Application.objects.filter(job=job).select_related('student')

        reports = []
        for app in applications:
            report = generate_match_report(app.student, job)
            report['application_id'] = app.id
            report['status'] = app.status
            report['cgpa'] = float(app.student.cgpa) if app.student.cgpa is not None else None
            reports.append(report)

        # Rank: eligible first, then highest skill match, then highest CGPA
        ranked_reports = sorted(
            reports,
            key=lambda r: (
                not r['overall_eligible'],
                -r['skill_match_percentage'],
                -(r['cgpa'] or 0),
            ),
        )

        for rank, report in enumerate(ranked_reports, start=1):
            report['rank'] = rank

        return Response(ranked_reports)


class SkillGapView(APIView):
    """
    GET -> skill-gap recommendations for the logged-in student and one job:
    which required skills are missing, ranked by how many other jobs
    the student is eligible for also ask for them.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_id):
        if request.user.role != 'STUDENT':
            return Response(
                {"detail": "Only students can request skill recommendations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        job = get_object_or_404(Job, pk=job_id)
        return Response(recommend_skills(request.user.student_profile, job))