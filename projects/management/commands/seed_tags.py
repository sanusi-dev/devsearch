"""
Management command that creates common developer tags if none exist.
Safe to run on every deploy — will be a no-op after the first run.
"""
from django.core.management.base import BaseCommand
from projects.models import Tag

DEFAULT_TAGS = [
    "Python", "JavaScript", "TypeScript", "React", "Django", "Node.js",
    "Vue", "Angular", "Next.js", "HTMX", "Tailwind CSS", "Docker",
    "Kubernetes", "AWS", "PostgreSQL", "MongoDB", "GraphQL", "Rust",
    "Go", "Flutter", "Swift", "Kotlin", "Terraform", "Machine Learning",
]


class Command(BaseCommand):
    help = "Seed common developer tags if none exist."

    def handle(self, *args, **options):
        if Tag.objects.exists():
            self.stdout.write("Tags already exist — skipping.")
            return

        created = 0
        for name in DEFAULT_TAGS:
            Tag.objects.get_or_create(name=name)
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} default tags."))
