from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            name = user.name,
            email = user.email,
            username = user.username,
        )

        subject = 'Account Successfully Registered'
        message = """
                    It is a long established fact that a reader will be distracted by the readable content of a 
                    page when looking at its layout.
                """
        recipient = instance.email
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
            fail_silently=False
        )
@receiver(post_save, sender=Profile)
def update_user(instance, created, *args, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.username = profile.username
        user.email = profile.email
        user.save()


