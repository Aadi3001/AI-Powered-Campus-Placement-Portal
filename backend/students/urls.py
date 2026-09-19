from django.urls import path
from .views import (MyStudentProfileView, EducationListCreateView, SkillListCreateView, ProjectListCreateView, InternshipListCreateView, CertificationListCreateView)


urlpatterns = [
    path('profile/', MyStudentProfileView.as_view(), name='my-student-profile'),
    path('education/', EducationListCreateView.as_view(), name='education-list-create'),
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('internships/', InternshipListCreateView.as_view(), name='internship-list-create'),
    path('certifications/', CertificationListCreateView.as_view(), name='certification-list-create'),
]