from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Review


@receiver([post_save, post_delete], sender=Review)
def update_project_vote(instance, *args, **kwargs):
    """Recalculate and persist vote_total and vote_ratio on the parent Project
    whenever a Review is created, updated, or deleted.
    """
    project = instance.project
    reviews = project.review_set.all()

    vote_total = reviews.count()
    up_votes = reviews.filter(value="up").count()

    project.vote_ratio = (up_votes / vote_total) * 100 if vote_total > 0 else 0
    project.vote_total = vote_total
    project.save()
