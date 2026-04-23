from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_htmx.http import HttpResponseClientRedirect, push_url
from .models import *
from .forms import *
from .utils import search_projects, pagination


def project_list(request):
    search_query, projects = search_projects(request)
    page_obj = pagination(request, projects)

    context = {"search_query": search_query, "page_obj": page_obj}

    if request.htmx:
        target = request.htmx.target
        if target == "main-content":
            return render(
                request, "projects/project_list.html#project-list-main", context
            )
        if target == "list-container":
            return render(
                request, "projects/project_list.html#project-list-partial", context
            )

    return render(request, "projects/project_list.html", context)


def project_detail(request, pk):
    project = get_object_or_404(Project, id=pk)
    review_form = ReviewForm()
    reviewers = project.review_set.select_related("owner").all()
    has_reviewed = (
        reviewers.filter(owner=request.user.profile).exists()
        if request.user.is_authenticated
        else False
    )

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.owner = request.user.profile
            review.project = project
            review.save()
            messages.success(request, 'Review submitted successfully!')

            # Re-fetch after save so the new review is included
            reviewers = project.review_set.select_related("owner").all()
            has_reviewed = True  # they just reviewed, no need to query again

            if request.htmx:
                context = {
                    "project": project,
                    "review_form": ReviewForm(),
                    "reviewers": reviewers,
                    "has_reviewed": has_reviewed,
                }
                return render(
                    request, "projects/project_detail.html#feedback-partial", context
                )

            return redirect("project_detail", pk=project.id)

        else:
            # On validation error, re-render just the form partial
            if request.htmx:
                context = {
                    "project": project,
                    "review_form": review_form,
                    "reviewers": reviewers,
                    "has_reviewed": has_reviewed,
                }
                return render(
                    request, "projects/project_detail.html#review-form-partial", context
                )

    context = {
        "project": project,
        "review_form": review_form,
        "reviewers": reviewers,
        "has_reviewed": has_reviewed,
    }

    if request.htmx:
        return render(
            request, "projects/project_detail.html#project-detail-partial", context
        )

    return render(request, "projects/project_detail.html", context)


@login_required(login_url="login")
def project_form(request, pk=None):
    profile = request.user.profile
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
            form.save_m2m()  # Ensure many-to-many fields (like tags) are saved
            
            action = "updated" if pk else "created"
            messages.success(request, f"Project '{new_project.title}' {action} successfully!")

            return redirect("account")

        # Validation errors — re-render the form partial with errors
        if request.htmx:
            context = {
                "form": form,
                "project": project,
                "form_title": form_title,
            }
            return render(
                request,
                "projects/project_create.html#project-form-partial",
                context,
            )

    context = {"form": form, "project": project, "form_title": form_title}

    if request.htmx:
        return render(
            request,
            "projects/project_create.html#project-form-partial",
            context,
        )

    return render(request, "projects/project_create.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    project = get_object_or_404(Project, id=pk, owner=request.user.profile)

    if request.method == "POST":
        project.delete()
        messages.success(request, f"Project '{project.title}' deleted successfully!")
        return redirect("account")

    return redirect("account")
