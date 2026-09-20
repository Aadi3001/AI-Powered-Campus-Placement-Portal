from django.urls import path
from .views import MyApplicationsView, JobApplicantsView, UpdateApplicationStatusView


urlpatterns = [
    path('my/', MyApplicationsView.as_view(), name='my-applications'),
    path('jobs/<int:job_id>/applicants/', JobApplicantsView.as_view(), name='job-applicants'),
    path('<int:pk>/status/', UpdateApplicationStatusView.as_view(), name='update-application-status'),
]