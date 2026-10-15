from django.urls import path
from .views import JobMatchReportView, SkillGapView

urlpatterns = [
    path('jobs/<int:job_id>/report/', JobMatchReportView.as_view(), name='job-match-report'),
    path('jobs/<int:job_id>/skill-gap/', SkillGapView.as_view(), name='skill-gap'),
]