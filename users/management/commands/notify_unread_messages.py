from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.signing import Signer
from django.utils import timezone
from users.models import Profile, Message
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends email notifications to users with unread messages'

    def handle(self, *args, **kwargs):
        profiles = Profile.objects.filter(receive_notifications=True)
        # print(profiles)
        signer = Signer()
        emails_sent = 0

        for profile in profiles:
            # Check for unread messages
            unread_count = Message.objects.filter(recipient=profile, is_read=False).count()
            # print(f"Unread count for {profile.email}: {unread_count}")
            if unread_count > 0:
                # Generate unsubscribe link
                signature = signer.sign(profile.id).split(':')[1]  # Get the signature part
                full_signature = f"{profile.id}:{signature}"
                unsubscribe_url = f"{settings.SITE_URL}/unsubscribe/{full_signature}/" if hasattr(settings, 'SITE_URL') else f"http://127.0.0.1:8000/unsubscribe/{full_signature}/"

                subject = f"You have {unread_count} unread message{'s' if unread_count > 1 else ''} on DevSearch"
                context = {
                    'profile': profile,
                    'unread_count': unread_count,
                    'unsubscribe_url': unsubscribe_url,
                }

                text_body = render_to_string("users/unread_message_email.txt", context)
                html_body = render_to_string("users/unread_message_email.html", context)

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[profile.email],
                )
                email.attach_alternative(html_body, "text/html")

                try:
                    email.send()
                    emails_sent += 1
                except Exception as e:
                    logger.exception("Failed to send unread message notification to %s: %s", profile.email, str(e))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully sent {emails_sent} unread message notifications.'))
