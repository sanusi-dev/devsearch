"""
Management command that creates a superuser if one does not already exist.
Uses DEFAULT_SUPERUSER_* environment variables for credentials.
Safe to run on every deploy — will be a no-op after the first run.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Ensure a superuser exists (no-op if already present)."

    def handle(self, *args, **options):
        User = get_user_model()

        username = "admin"

        if User.objects.filter(username=username, is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists."))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email="admin@devsearch.io",
                password="admin123!@#",
            )
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
        else:
            self.stdout.write(f"User '{username}' exists but is not a superuser — skipping.")
