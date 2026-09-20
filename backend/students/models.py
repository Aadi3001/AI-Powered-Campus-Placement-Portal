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

    full_name = models.CharField(max_length=150, blank=True, default='')
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    degree = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
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


class Skill(models.Model):
    """
    A single skill claimed by a student (e.g. "Python", "React").
    A student can have many skills.
    """
    PROFICIENCY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='skills',
    )
    name = models.CharField(max_length=100)
    proficiency = models.CharField(
        max_length=20,
        choices=PROFICIENCY_CHOICES,
        default='INTERMEDIATE',
    )

    def __str__(self):
        return f"{self.name} ({self.proficiency}) - {self.student.full_name}"


class Project(models.Model):
    """
    A project a student has worked on.
    A student can have many projects.
    """
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    technologies_used = models.CharField(max_length=300, blank=True)  # e.g. "Django, React, PostgreSQL"
    project_link = models.URLField(blank=True)  # e.g. GitHub or live demo link

    def __str__(self):
        return f"{self.title} - {self.student.full_name}"


class Internship(models.Model):
    """
    An internship a student has completed or is doing.
    A student can have many internships.
    """
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='internships',
    )
    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null = ongoing
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.role} at {self.company_name} - {self.student.full_name}"


class Certification(models.Model):
    """
    A certification/course a student has completed.
    A student can have many certifications.
    """
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='certifications',
    )
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.student.full_name}"