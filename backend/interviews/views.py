from rest_framework import generics

from accounts.permissions import IsRecruiter, IsStudent
from notifications.utils import notify

from .models import Interview
from .serializers import (
    InterviewSerializer,
    ScheduleInterviewSerializer,
    UpdateInterviewSerializer,
)

# Related rows fetched together, to avoid one extra query per interview
RELATED = ('application__job__recruiter__company', 'application__student')


class ScheduleInterviewView(generics.CreateAPIView):
    """POST -> a recruiter schedules an interview for a shortlisted applicant."""
    serializer_class = ScheduleInterviewSerializer
    permission_classes = [IsRecruiter]

    def perform_create(self, serializer):
        interview = serializer.save()
        application = interview.application
        notify(
            application.student.user,
            f'An interview ({interview.round_name}) was scheduled for '
            f'"{application.job.title}". Open My interviews for the date and time.',
            '/student/interviews',
        )


class MyInterviewsView(generics.ListAPIView):
    """GET -> the logged-in student's interviews, soonest first."""
    serializer_class = InterviewSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Interview.objects.filter(
            application__student=self.request.user.student_profile
        ).select_related(*RELATED)


class JobInterviewsView(generics.ListAPIView):
    """GET -> interviews for one of the logged-in recruiter's own jobs."""
    serializer_class = InterviewSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        return Interview.objects.filter(
            application__job_id=self.kwargs['job_id'],
            application__job__recruiter=self.request.user.recruiter_profile,
        ).select_related(*RELATED)


class UpdateInterviewView(generics.UpdateAPIView):
    """PATCH -> a recruiter reschedules, cancels or completes their own interview."""
    serializer_class = UpdateInterviewSerializer
    permission_classes = [IsRecruiter]
    http_method_names = ['patch', 'options']

    def get_queryset(self):
        return Interview.objects.filter(
            application__job__recruiter=self.request.user.recruiter_profile
        )

    def perform_update(self, serializer):
        before_time = serializer.instance.scheduled_at
        before_status = serializer.instance.status
        interview = serializer.save()
        application = interview.application

        if interview.status == 'CANCELLED' and before_status != 'CANCELLED':
            notify(
                application.student.user,
                f'Your interview ({interview.round_name}) for '
                f'"{application.job.title}" was cancelled.',
                '/student/interviews',
            )
        elif interview.scheduled_at != before_time:
            notify(
                application.student.user,
                f'Your interview ({interview.round_name}) for '
                f'"{application.job.title}" was rescheduled. '
                'Open My interviews for the new time.',
                '/student/interviews',
            )