from django.urls import path
from .views import MyStudentProfileView, EducationListCreateView

urlpatterns = [
    path('profile/', MyStudentProfileView.as_view(), name='my-student-profile'),
    path('education/', EducationListCreateView.as_view(), name='education-list-create'),
]