from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_user_profile(sender, instance, created, **kwargs):
    if created:
        from .models import UserProfile
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={"role": UserProfile.Role.ORGANIZER if instance.is_superuser else UserProfile.Role.CANDIDATE},
        )
