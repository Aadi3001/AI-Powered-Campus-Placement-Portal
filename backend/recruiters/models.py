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
    null=True,
    blank=True,
    )
    full_name = models.CharField(max_length=150, blank=True, default='')
    designation = models.CharField(max_length=150, blank=True)  # e.g. "HR Manager"
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        company_name = self.company.name if self.company else "No company yet"
        return f"{self.full_name or 'Unnamed'} - {company_name}"


class SkillTag(models.Model):
    """
    A single reusable skill name (e.g. "Python", "React").
    Used as a master list that Jobs (and later, matching logic) reference.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    """
    A job posting / placement drive created by a recruiter.
    """
    recruiter = models.ForeignKey(
        RecruiterProfile,
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()

    required_skills = models.ManyToManyField(
        SkillTag,
        related_name='jobs_requiring',
        blank=True,
    )

    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    eligible_branches = models.CharField(max_length=300, blank=True)  # comma-separated for now
    min_graduation_year = models.PositiveIntegerField(null=True, blank=True)
    max_graduation_year = models.PositiveIntegerField(null=True, blank=True)

    location = models.CharField(max_length=150, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)  # e.g. "6-8 LPA"

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.recruiter.company}"