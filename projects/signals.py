from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *


@receiver([post_save, post_delete], sender=Review)
def update_project_vote(instance, *args, **kwargs):
    project = instance.project

    reviews = project.review_set.all()

    vote_total = reviews.count()
    up_votes = reviews.filter(value='up').count()

    if vote_total > 0:
        vote_ratio = (up_votes/vote_total) * 100
    else:
        vote_ratio = 0

    project.vote_ratio = vote_ratio
    project.vote_total = vote_total
    project.save()


