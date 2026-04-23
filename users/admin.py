from django.contrib import admin

from .models import Profile, Skill, Message


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email", "signup_method", "receive_notifications", "created_at")
    search_fields = ("name", "email", "username")
    list_filter = ("signup_method", "receive_notifications")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "subject", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("sender__name", "recipient__name", "subject")
