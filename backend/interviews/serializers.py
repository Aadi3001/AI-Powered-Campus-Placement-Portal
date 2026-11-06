from django.utils import timezone
from rest_framework import serializers

from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):
    """For reading: includes the job, company and student for display."""
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    company_name = serializers.CharField(
        source='application.job.recruiter.company.name',
        read_only=True,
        allow_null=True,
    )
    student_name = serializers.CharField(
        source='application.student.full_name', read_only=True
    )

    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'job_title', 'company_name', 'student_name',
            'round_name', 'scheduled_at', 'mode', 'location_or_link',
            'notes', 'status',
        ]
        read_only_fields = fields


def must_be_in_the_future(value):
    if value <= timezone.now():
        raise serializers.ValidationError('Pick a date and time in the future.')
    return value


class ScheduleInterviewSerializer(serializers.ModelSerializer):
    """For scheduling: enforces ownership, shortlisting and a future time."""

    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'round_name', 'scheduled_at',
            'mode', 'location_or_link', 'notes',
        ]

    def validate_application(self, application):
        recruiter = self.context['request'].user.recruiter_profile
        if application.job.recruiter_id != recruiter.id:
            raise serializers.ValidationError(
                'You can only schedule interviews for applicants to your own jobs.'
            )
        if application.status != 'SHORTLISTED':
            raise serializers.ValidationError(
                'Shortlist the candidate before scheduling an interview.'
            )
        return application

    def validate_scheduled_at(self, value):
        return must_be_in_the_future(value)


class UpdateInterviewSerializer(serializers.ModelSerializer):
    """For changing an existing interview (reschedule, cancel, complete)."""

    class Meta:
        model = Interview
        fields = [
            'round_name', 'scheduled_at', 'mode',
            'location_or_link', 'notes', 'status',
        ]

    def validate_scheduled_at(self, value):
        return must_be_in_the_future(value)