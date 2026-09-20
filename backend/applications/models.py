from django.db import models
from students.models import StudentProfile
from recruiters.models import Job


class Application(models.Model):
    """
    Represents a student's application to a specific job.
    A student can apply to a job only once (enforced below).
    """

    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('REJECTED', 'Rejected'),
        ('SELECTED', 'Selected'),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='APPLIED',
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'job'],
                name='unique_student_job_application',
            )
        ]

    def __str__(self):
        return f"{self.student.full_name} -> {self.job.title} ({self.status})"