from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from students.models import StudentProfile
from recruiters.models import RecruiterProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_role_profile(sender, instance, created, **kwargs):
    """
    Whenever a new User is created, automatically create the matching
    empty profile based on their role.
    """
    if not created:
        return  # only act on NEW users, not every save/update

    if instance.role == 'STUDENT':
        StudentProfile.objects.create(user=instance)
    elif instance.role == 'RECRUITER':
        RecruiterProfile.objects.create(user=instance)
    # TPO and ADMIN roles don't get an auto-created profile (not needed yet)