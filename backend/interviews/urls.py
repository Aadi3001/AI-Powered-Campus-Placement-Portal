from django.urls import path

from .views import (
    JobInterviewsView,
    MyInterviewsView,
    ScheduleInterviewView,
    UpdateInterviewView,
)

urlpatterns = [
    path('schedule/', ScheduleInterviewView.as_view(), name='interview-schedule'),
    path('my/', MyInterviewsView.as_view(), name='interview-my'),
    path('jobs/<int:job_id>/', JobInterviewsView.as_view(), name='interview-job'),
    path('<int:pk>/', UpdateInterviewView.as_view(), name='interview-update'),
]