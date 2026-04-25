from django.contrib import admin

from .models import Project, Review, Tag


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "vote_ratio", "vote_total", "created_at")
    search_fields = ("title", "owner__name", "description")
    list_filter = ("tags",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("project", "owner", "value", "created_at")
    list_filter = ("value",)
    search_fields = ("project__title", "owner__name")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)