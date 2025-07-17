from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from .models import Course, Subject
from django.core.cache import cache

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)

@receiver([post_delete, post_save], sender=Subject)
def course_list_cache_update(sender, instance=None, created=False, **kwargs):
    cache.clear()

@receiver([post_delete, post_save], sender=Subject)
def subject_list_cache_update(sender, instance=None, created=False, **kwargs):
    cache.clear()

