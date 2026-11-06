from django.db import models

from applications.models import Application


class Interview(models.Model):
    """One interview round for an application. An application can have several."""

    MODE_CHOICES = [('ONLINE', 'Online'), ('ONSITE', 'On site')]
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='interviews',
    )
    round_name = models.CharField(max_length=100, default='Interview')  # e.g. Technical, HR
    scheduled_at = models.DateTimeField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='ONLINE')
    location_or_link = models.CharField(max_length=300, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at', 'id']

    def __str__(self):
        return f'{self.round_name} - {self.application}'