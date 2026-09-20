from django.urls import path
from .views import (CompanyListCreateView, MyRecruiterProfileView)


urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('profile/', MyRecruiterProfileView.as_view(), name='recruiter-profile-list-create'),
]