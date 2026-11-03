from django.conf import settings
from django.db import models


class Notification(models.Model):
    """A short in-app message for one user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=200, blank=True)  # a page in the React app
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.user.username}: {self.message}"