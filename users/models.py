from django.db import models
import uuid
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.TextField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True, default='profiles/user-default.png')
    social_github = models.URLField(null=True, blank=True)
    social_twitter = models.URLField(null=True, blank=True)
    social_linkedin = models.URLField(null=True, blank=True)
    social_youtube = models.URLField(null=True, blank=True)
    social_website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return str(self.user.username.title())
    

class Skill(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return str(self.name) if self.name else ''
    

class Message(models.Model):
    sender = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=500, blank=True, null=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return f'{self.sender}'
    
    class Meta:
        ordering = ['is_read', '-created_at']

        constraints = [
            models.CheckConstraint(
                condition=~models.Q(sender=models.F('recipient')),
                name='prevent_self_message'
            )
        ]
