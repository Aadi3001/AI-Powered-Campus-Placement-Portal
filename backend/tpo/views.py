from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsTPO
from applications.models import Application
from prediction.persistence import load_metadata
from recruiters.models import Company, Job, RecruiterProfile
from students.models import BRANCH_CHOICES, StudentProfile

BRANCH_LABELS = dict(BRANCH_CHOICES)


class StatsView(APIView):
    """GET -> placement statistics for the TPO dashboard."""
    permission_classes = [IsTPO]

    def get(self, request):
        total_students = StudentProfile.objects.count()
        placed_students = (
            Application.objects.filter(status='SELECTED')
            .values('student').distinct().count()
        )

        application_status = {
            row['status']: row['n']
            for row in Application.objects.values('status').annotate(n=Count('id'))
        }

        by_branch = (
            StudentProfile.objects.values('branch')
            .annotate(
                total=Count('id', distinct=True),
                placed=Count(
                    'id', filter=Q(applications__status='SELECTED'), distinct=True
                ),
            )
            .order_by('-total')
        )

        top_companies = (
            Application.objects.filter(status='SELECTED')
            .exclude(job__recruiter__company__isnull=True)
            .values('job__recruiter__company__name')
            .annotate(selected=Count('id'))
            .order_by('-selected')[:5]
        )

        busiest_jobs = (
            Job.objects.annotate(
                applicants=Count('applications'),
                selected=Count('applications', filter=Q(applications__status='SELECTED')),
            )
            .select_related('recruiter__company')
            .order_by('-applicants')[:5]
        )

        try:
            metadata = load_metadata()
            model_info = {
                'features': metadata['features'],
                'rows_total': metadata['rows_total'],
                'rows_test_split': metadata['rows_test_split'],
                'test_metrics': metadata['test_metrics'],
                'baseline_metrics': metadata['baseline_metrics'],
                'saved_at': metadata['saved_at'],
                'note': metadata['note'],
            }
        except FileNotFoundError:
            model_info = None

        return Response({
            'totals': {
                'students': total_students,
                'recruiters': RecruiterProfile.objects.count(),
                'companies': Company.objects.count(),
                'jobs': Job.objects.count(),
                'open_jobs': Job.objects.filter(is_active=True).count(),
                'applications': Application.objects.count(),
            },
            'placement': {
                'students_placed': placed_students,
                'placement_rate': (
                    round(100 * placed_students / total_students, 1)
                    if total_students else 0
                ),
            },
            'application_status': application_status,
            'by_branch': [
                {
                    'branch': row['branch'] or 'NOT_SET',
                    'label': BRANCH_LABELS.get(row['branch'], 'Not set'),
                    'total': row['total'],
                    'placed': row['placed'],
                }
                for row in by_branch
            ],
            'top_companies': [
                {'company': row['job__recruiter__company__name'], 'selected': row['selected']}
                for row in top_companies
            ],
            'busiest_jobs': [
                {
                    'job': job.title,
                    'company': job.recruiter.company.name if job.recruiter.company else None,
                    'applicants': job.applicants,
                    'selected': job.selected,
                }
                for job in busiest_jobs
            ],
            'model': model_info,
        })