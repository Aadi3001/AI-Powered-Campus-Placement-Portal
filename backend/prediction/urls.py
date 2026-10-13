from django.urls import path
from .views import MyChanceView

urlpatterns = [
    path('jobs/<int:job_id>/my-chance/', MyChanceView.as_view(), name='my-chance'),
]