from django.db import models
import uuid
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, default="")
    email = models.EmailField(max_length=254, blank=True, default="")
    username = models.CharField(max_length=200, blank=True, default="")
    location = models.CharField(max_length=200, blank=True, default="")
    short_intro = models.CharField(max_length=200, blank=True, default="")
    bio = models.TextField(blank=True, default="")
    profile_image = models.ImageField(upload_to="profiles/", blank=True, default="default_profile.svg")
    social_github = models.URLField(blank=True, default="")
    social_twitter = models.URLField(blank=True, default="")
    social_linkedin = models.URLField(blank=True, default="")
    social_youtube = models.URLField(blank=True, default="")
    social_website = models.URLField(blank=True, default="")
    signup_method = models.CharField(max_length=50, blank=True, default="email")
    receive_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.user:
            return self.user.username.title() if self.user.username else self.user.email
        return self.name or self.email or str(self.id)
class Skill(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name) if self.name else ""

class Message(models.Model):
    sender = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=500, blank=True, null=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        if self.sender:
            return f"Message from {self.sender.name or self.sender.email} — {self.subject or 'No subject'}"
        return f"Message from {self.name or self.email} — {self.subject or 'No subject'}"

    class Meta:
        ordering = ["is_read", "-created_at"]

        constraints = [
            models.CheckConstraint(
                condition=~models.Q(sender=models.F('recipient')),
                name='prevent_self_message'
            )
        ]
