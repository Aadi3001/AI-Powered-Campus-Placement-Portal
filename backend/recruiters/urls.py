from django.urls import path
from .views import (
    CompanyListCreateView, MyRecruiterProfileView, SkillTagListCreateView,
    JobListCreateView, MyJobsView,
)


urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('profile/', MyRecruiterProfileView.as_view(), name='recruiter-profile-list-create'),
    path('skills/', SkillTagListCreateView.as_view(), name='skill-list-create'),
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('my-jobs/', MyJobsView.as_view(), name='my-jobs'),
]