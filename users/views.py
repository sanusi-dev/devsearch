from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Prefetch
from django.core.signing import Signer, BadSignature

from allauth.account.forms import LoginForm, SignupForm
from allauth.account.views import LoginView, SignupView
from django_htmx.http import retarget

from projects.models import Project
from .models import Profile, Skill, Message
from .forms import ProfileForm, SkillForm, MessageForm
from .utils import search_profiles
from projects.utils import pagination


def _get_user_profile(request):
    """Safely retrieve the current user's profile, or return 404."""
    return get_object_or_404(Profile, user=request.user)


def signup_view(request):
    """Render the signup page, or redirect if already authenticated."""
    if request.user.is_authenticated:
        return redirect("profile_list")

    context = {"form": SignupForm()}

    if request.htmx:
        return render(request, "account/signup.html#signup-form-partial", context)

    return render(request, "account/signup.html", context)


def login_view(request):
    """Render the login page, or redirect if already authenticated."""
    if request.user.is_authenticated:
        return redirect("profile_list")

    context = {"form": LoginForm()}

    if request.htmx:
        return render(request, "account/login.html#login-form-partial", context)

    return render(request, "account/login.html", context)


def logout_user(request):
    """Log out the current user and redirect to the login page."""
    logout(request)
    return redirect("login")


class CustomLoginView(LoginView):
    """All auth login view override — returns partial HTML on HTMX validation errors."""

    def form_invalid(self, form):
        if self.request.htmx:
            response = render(
                self.request, "account/login.html#login-form-partial", {"form": form}
            )
            return retarget(response, "#login-container")
        return super().form_invalid(form)


class CustomSignupView(SignupView):
    """All auth signup view override — returns partial HTML on HTMX validation errors."""

    def form_invalid(self, form):
        if self.request.htmx:
            response = render(
                self.request, "account/signup.html#signup-form-partial", {"form": form}
            )
            return retarget(response, "#signup-container")
        return super().form_invalid(form)


def profile_list(request):
    """List developer profiles with search and pagination."""
    search_query, profiles = search_profiles(request)
    page_obj = pagination(request, profiles)

    context = {"page_obj": page_obj, "search_query": search_query}

    if request.htmx:
        target = request.htmx.target
        if target == "main-content":
            return render(request, "users/profile_list.html#profile-list-main", context)
        if target == "list-container":
            return render(request, "users/profile_list.html#profile-list-partial", context)

    return render(request, "users/profile_list.html", context)


def profile_detail(request, pk):
    """Show a single developer profile with skills and projects."""
    profile = get_object_or_404(
        Profile.objects.prefetch_related(
            Prefetch("skill_set", queryset=Skill.objects.order_by("name")),
            Prefetch("project_set", queryset=Project.objects.prefetch_related("tags")),
        ),
        id=pk,
    )
    context = {"profile": profile}

    if request.htmx:
        return render(request, "users/profile_detail.html#profile-detail-partial", context)

    return render(request, "users/profile_detail.html", context)


@login_required(login_url="login")
def user_account(request):
    """Show the current user's account dashboard with skills, projects, and stats."""
    profile, _created = Profile.objects.get_or_create(user=request.user)
    # Prefetch related objects to avoid N+1 queries in the template.
    profile = (
        Profile.objects.filter(id=profile.id)
        .prefetch_related(
            Prefetch("skill_set", queryset=Skill.objects.order_by("name")),
            Prefetch("project_set", queryset=Project.objects.prefetch_related("tags")),
            "messages",
        )
        .first()
    )
    context = {"profile": profile}

    if request.htmx:
        return render(request, "users/user_account.html#user-account-partial", context)

    return render(request, "users/user_account.html", context)


@login_required(login_url="login")
def profile_edit(request):
    """Edit the current user's profile."""
    profile = _get_user_profile(request)
    profile_form = ProfileForm(instance=profile)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("account")

        if request.htmx:
            context = {"profile_form": profile_form}
            return render(request, "users/profile_form.html#profile-form-partial", context)

    context = {"profile_form": profile_form}

    if request.htmx:
        return render(request, "users/profile_form.html#profile-form-partial", context)

    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def skill_form(request, pk=None):
    """Create or edit a skill for the current user's profile."""
    profile = _get_user_profile(request)
    skill = get_object_or_404(Skill, id=pk, owner=profile) if pk else None
    form_title = "Edit Skill" if pk else "Add Skill"

    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            new_skill = form.save(commit=False)
            new_skill.owner = profile
            new_skill.save()
            action = "updated" if pk else "added"
            messages.success(request, f"Skill '{new_skill.name}' {action} successfully!")
            return redirect("account")

        if request.htmx:
            context = {"form": form, "skill": skill, "form_title": form_title}
            return render(request, "users/skill_create.html#skill-form-partial", context)

    context = {"form": form, "skill": skill, "form_title": form_title}

    if request.htmx:
        return render(request, "users/skill_create.html#skill-form-partial", context)

    return render(request, "users/skill_create.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    """Delete a skill owned by the current user."""
    profile = _get_user_profile(request)
    skill = get_object_or_404(Skill, id=pk, owner=profile)

    if request.method == "POST":
        skill_name = skill.name
        skill.delete()
        messages.success(request, f"Skill '{skill_name}' deleted successfully!")
        return redirect("account")

    return redirect("account")


@login_required(login_url="login")
def inbox(request):
    """Show the current user's message inbox."""
    profile = _get_user_profile(request)
    un_read = Message.objects.filter(recipient=profile, is_read=False).count()
    context = {"profile": profile, "un_read": un_read}

    if request.htmx:
        return render(request, "users/inbox.html#inbox-partial", context)

    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def message(request, pk):
    """Show a single message sent to the current user."""
    profile = _get_user_profile(request)
    msg = get_object_or_404(Message, id=pk, recipient=profile)

    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=["is_read"])

    context = {"message": msg}

    if request.htmx:
        return render(request, "users/message.html#message-detail-partial", context)

    return render(request, "users/message.html", context)


@login_required(login_url="login")
def delete_message(request, pk):
    """Delete a message sent to the current user."""
    profile = _get_user_profile(request)
    msg = get_object_or_404(Message, id=pk, recipient=profile)

    if request.method == "POST":
        msg.delete()
        messages.success(request, "Message deleted successfully!")
        return redirect("inbox")

    return redirect("inbox")


def send_message(request, pk):
    """Send a message to a developer profile."""
    recipient = get_object_or_404(Profile, id=pk)
    message_form = MessageForm()

    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            msg = message_form.save(commit=False)
            if request.user.is_authenticated:
                sender_profile, _ = Profile.objects.get_or_create(user=request.user)
                msg.sender = sender_profile
                msg.name = sender_profile.name
                msg.email = sender_profile.email
            msg.recipient = recipient
            msg.save()
            messages.success(request, "Message sent successfully!")
            return redirect("profile_detail", pk=recipient.id)

        if request.htmx:
            context = {"message_form": message_form, "recipient": recipient}
            return render(request, "users/send_message.html#send-message-partial", context)

    context = {"message_form": message_form, "recipient": recipient}

    if request.htmx:
        return render(request, "users/send_message.html#send-message-partial", context)

    return render(request, "users/send_message.html", context)


def unsubscribe(request, signature):
    """Process an unsubscribe link from notification emails."""
    signer = Signer()
    try:
        profile_id = signer.unsign(signature)
        profile = get_object_or_404(Profile, id=profile_id)
        profile.receive_notifications = False
        profile.save(update_fields=["receive_notifications"])
        messages.success(
            request, "You have been successfully unsubscribed from email notifications."
        )
    except BadSignature:
        messages.error(request, "Invalid or expired unsubscribe link.")

    return redirect("login")
