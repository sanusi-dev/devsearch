import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from allauth.account.signals import user_signed_up

from .models import *

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    """Create a bare Profile whenever a new User is saved.

    This fires for both email/password signups and GitHub OAuth signups.
    The profile is intentionally minimal here — the ``user_signed_up``
    handler below fills in provider-specific data and sends the welcome email.
    """
    if created:
        user = instance
        # Build a sensible display name from whatever is available
        name = (
            getattr(user, "name", "")
            or f"{user.first_name} {user.last_name}".strip()
            or user.email
            or user.username
        )
        Profile.objects.create(
            user=user,
            name=name,
            email=user.email,
            username=user.username,
        )


@receiver(user_signed_up)
def handle_allauth_signup(request, user, **kwargs):
    """Runs after allauth finishes creating and logging in a new user.

    At this point the Profile already exists (created by ``create_profile``
    above).  This handler:
      1. Patches the profile with richer data from the social provider
         (if it was a GitHub signup).
      2. Sends the welcome email.
    """
    profile = user.profile

    sociallogin = kwargs.get("sociallogin")
    if sociallogin:
        extra = sociallogin.account.extra_data
        # GitHub provides 'name', 'login', 'email', 'avatar_url', etc.
        profile.name = extra.get("name") or extra.get("login") or profile.name
        profile.email = sociallogin.user.email or profile.email
        profile.username = extra.get("login") or profile.username
        profile.social_github = extra.get("html_url", "")
        profile.signup_method = sociallogin.account.provider.title()
        profile.save()

    send_welcome_email(profile)


def send_welcome_email(profile):
    """Send a welcome email to a newly registered user.

    Uses Django's EmailMultiAlternatives for proper HTML + plaintext support.
    django-mailer intercepts this via EMAIL_BACKEND and queues it in the DB.
    """
    subject = "Welcome to DevSearch!"
    context = {
        "profile": profile,
        "signup_method": profile.signup_method or "Email"
    }

    text_body = render_to_string("users/welcome_email.txt", context)
    html_body = render_to_string("users/welcome_email.html", context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[profile.email],
    )
    email.attach_alternative(html_body, "text/html")

    try:
        email.send()
    except Exception:
        logger.exception("Failed to queue welcome email for %s", profile.email)


@receiver(post_save, sender=Profile)
def update_user(instance, created, *args, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.username = profile.username
        user.email = profile.email
        user.save()
