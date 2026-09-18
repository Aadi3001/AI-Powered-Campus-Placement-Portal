from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.
    Adds a 'role' field so we know whether this user is a
    Student, Recruiter, TPO, or Admin.
    """

    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        RECRUITER = 'RECRUITER', 'Recruiter'
        TPO = 'TPO', 'TPO'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"