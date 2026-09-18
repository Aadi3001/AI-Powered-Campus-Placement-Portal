from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    """
    Extends a User (role=STUDENT) with student-specific details.
    One-to-one: each user has exactly one student profile.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
    )

    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    degree = models.CharField(max_length=100)          # e.g. "B.Tech"
    branch = models.CharField(max_length=100)           # e.g. "Computer Engineering"
    graduation_year = models.PositiveIntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"


class Education(models.Model):
    """
    One education record (e.g. 10th, 12th, Bachelor's).
    A student can have multiple Education entries.
    """
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='education',
    )

    level = models.CharField(max_length=100)          # e.g. "10th", "12th", "Bachelor's"
    institution = models.CharField(max_length=200)
    board_or_university = models.CharField(max_length=200, blank=True)
    percentage_or_cgpa = models.DecimalField(max_digits=5, decimal_places=2)
    year_of_completion = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.level} - {self.institution} ({self.student.full_name})"