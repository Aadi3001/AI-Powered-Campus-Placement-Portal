from django.urls import path
from .views import MyStudentProfileView

urlpatterns = [
    path('profile/', MyStudentProfileView.as_view(), name='my-student-profile'),
]