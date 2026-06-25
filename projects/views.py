from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
from django_htmx.http import HttpResponseClientRedirect, push_url

from users.models import Profile
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, pagination


def _get_user_profile(request):
    """Safely retrieve the current user's profile, or return 404."""
    return get_object_or_404(Profile, user=request.user)


def project_list(request):
    """List projects with search and pagination."""
    search_query, projects = search_projects(request)
    page_obj = pagination(request, projects)

    context = {"search_query": search_query, "page_obj": page_obj}

    if request.htmx:
        target = request.htmx.target
        if target == "main-content":
            return render(request, "projects/project_list.html#project-list-main", context)
        if target == "list-container":
            return render(request, "projects/project_list.html#project-list-partial", context)

    return render(request, "projects/project_list.html", context)


def project_detail(request, pk):
    """Show a single project with reviews and feedback form."""
    project = get_object_or_404(
        Project.objects.prefetch_related("tags"),
        id=pk,
    )
    review_form = ReviewForm()
    reviewers = project.review_set.select_related("owner").all()
    has_reviewed = (
        request.user.is_authenticated
        and reviewers.filter(owner__user=request.user).exists()
    )

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.owner = _get_user_profile(request)
            review.project = project
            review.save()
            messages.success(request, "Review submitted successfully!")

            reviewers = project.review_set.select_related("owner").all()
            has_reviewed = True

            if request.htmx:
                context = {
                    "project": project,
                    "review_form": ReviewForm(),
                    "reviewers": reviewers,
                    "has_reviewed": has_reviewed,
                }
                return render(request, "projects/project_detail.html#feedback-partial", context)

            return redirect("project_detail", pk=project.id)

        if request.htmx:
            context = {
                "project": project,
                "review_form": review_form,
                "reviewers": reviewers,
                "has_reviewed": has_reviewed,
            }
            return render(request, "projects/project_detail.html#review-form-partial", context)

    context = {
        "project": project,
        "review_form": review_form,
        "reviewers": reviewers,
        "has_reviewed": has_reviewed,
    }

    if request.htmx:
        return render(request, "projects/project_detail.html#project-detail-partial", context)

    return render(request, "projects/project_detail.html", context)


@login_required(login_url="login")
def project_form(request, pk=None):
    """Create or edit a project for the current user's profile."""
    profile = _get_user_profile(request)
    project = get_object_or_404(Project, id=pk) if pk else None

    if project and project.owner != profile:
        return redirect("profile_list")

    form_title = "Update Project" if pk else "Create Project"
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = profile
            new_project.save()
            form.save_m2m()

            action = "updated" if pk else "created"
            messages.success(request, f"Project '{new_project.title}' {action} successfully!")
            return redirect("account")

        if request.htmx:
            context = {"form": form, "project": project, "form_title": form_title}
            return render(request, "projects/project_create.html#project-form-partial", context)

    context = {"form": form, "project": project, "form_title": form_title}

    if request.htmx:
        return render(request, "projects/project_create.html#project-form-partial", context)

    return render(request, "projects/project_create.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    """Delete a project owned by the current user."""
    profile = _get_user_profile(request)
    project = get_object_or_404(Project, id=pk, owner=profile)

    if request.method == "POST":
        project_title = project.title
        project.delete()
        messages.success(request, f"Project '{project_title}' deleted successfully!")
        return redirect("account")

    return redirect("account")
