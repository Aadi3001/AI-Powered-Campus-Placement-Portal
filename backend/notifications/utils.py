from .models import Notification


def notify(user, message, link=''):
    """Creates an in-app notification for one user."""
    return Notification.objects.create(user=user, message=message[:255], link=link)