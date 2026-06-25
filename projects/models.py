from django.db import models
import uuid

from users.models import Profile
class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.URLField(null=True, blank=True, max_length=2000)
    source_link = models.URLField(null=True, blank=True, max_length=2000)
    featured_image = models.ImageField(upload_to="projects/", null=True, blank=True, default="default_project.svg")

    @property
    def image_url(self):
        """Return the project image URL, falling back to the default if unset or stale."""
        if self.featured_image and self.featured_image.name:
            if self.featured_image.name == "default.jpg":
                return "https://s3.us-east-005.backblazeb2.com/devsearchh/default_project.svg"
            return self.featured_image.url
        return "https://s3.us-east-005.backblazeb2.com/devsearchh/default_project.svg"
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(null=True, default=0, blank=True)
    vote_ratio = models.IntegerField(null=True, default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title.title()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'up vote'),
        ('down', 'down vote')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE) 
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["project", "owner"]]

    def __str__(self):
        return f"{self.value} vote by {self.owner.name if self.owner else 'Unknown'} on {self.project.title if self.project else 'Unknown'}"


class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.title()
