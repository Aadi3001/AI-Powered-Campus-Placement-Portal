from django.conf import settings
from django.db import models


class Company(models.Model):
    """
    A company that posts jobs/placement drives.
    Multiple recruiters can belong to the same company.
    """
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)

    def __str__(self):
        return self.name


class RecruiterProfile(models.Model):
    """
    Extends a User (role=RECRUITER) with recruiter-specific details.
    One-to-one with User; many-to-one with Company.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recruiter_profile',
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='recruiters',
    )
    full_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150, blank=True)  # e.g. "HR Manager"
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.company.name}"