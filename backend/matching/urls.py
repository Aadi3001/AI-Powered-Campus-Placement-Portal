from django.urls import path
from .views import JobMatchReportView

urlpatterns = [
    path('jobs/<int:job_id>/report/', JobMatchReportView.as_view(), name='job-match-report'),
]