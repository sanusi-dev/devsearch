from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.signing import Signer, BadSignature

from allauth.account.forms import LoginForm, SignupForm
from allauth.account.views import LoginView, SignupView
from django_htmx.http import retarget

from .models import *
from .forms import *
from .utils import search_profiles
from projects.utils import pagination


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("profile_list")
    
    context = {
        "form": SignupForm(),
    }
    
    if request.htmx:
        return render(request, "account/signup.html#signup-form-partial", context)
    
    return render(request, "account/signup.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("profile_list")
    
    context = {
        "form": LoginForm(),
    }

    if request.htmx:
        return render(request, "account/login.html#login-form-partial", context)
    
    return render(request, "account/login.html", context)

def logout_user(request):
    logout(request)
    return redirect("login")

class CustomLoginView(LoginView):
    
    def form_invalid(self, form):
        if self.request.htmx:
            response = render(
                self.request, "account/login.html#login-form-partial", {"form": form}
            )
            return retarget(response, "#login-container")
        return super().form_invalid(form)


class CustomSignupView(SignupView):
    def form_invalid(self, form):
        if self.request.htmx:
            response = render(
                self.request, "account/signup.html#signup-form-partial", {"form": form}
            )
            return retarget(response, "#signup-container")
        return super().form_invalid(form)


def profile_list(request):
    search_query, profiles = search_profiles(request)
    page_obj = pagination(request, profiles)

    context = {"page_obj": page_obj, "search_query": search_query}

    if request.htmx:
        target = request.htmx.target
        if target == "main-content":
            return render(request, "users/profile_list.html#profile-list-main", context)
        if target == "list-container":
            return render(
                request, "users/profile_list.html#profile-list-partial", context
            )

    return render(request, "users/profile_list.html", context)


def profile_detail(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    context = {"profile": profile}

    if request.htmx:
        return render(
            request, "users/profile_detail.html#profile-detail-partial", context
        )

    return render(request, "users/profile_detail.html", context)


@login_required(login_url="login")
def user_account(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {"profile": profile}

    if request.htmx:
        return render(request, "users/user_account.html#user-account-partial", context)

    return render(request, "users/user_account.html", context)


@login_required(login_url="login")
def profile_edit(request):
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect("account")

        # Validation errors — re-render form partial
        if request.htmx:
            context = {"profile_form": profile_form}
            return render(
                request, "users/profile_form.html#profile-form-partial", context
            )

    context = {"profile_form": profile_form}

    if request.htmx:
        return render(request, "users/profile_form.html#profile-form-partial", context)

    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def skill_form(request, pk=None):
    profile = request.user.profile
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

        # Validation errors — re-render form partial
        if request.htmx:
            context = {"form": form, "skill": skill, "form_title": form_title}
            return render(
                request, "users/skill_create.html#skill-form-partial", context
            )

    context = {"form": form, "skill": skill, "form_title": form_title}

    if request.htmx:
        return render(request, "users/skill_create.html#skill-form-partial", context)

    return render(request, "users/skill_create.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, id=pk, owner=request.user.profile)

    if request.method == "POST":
        skill.delete()
        messages.success(request, f"Skill '{skill.name}' deleted successfully!")
        return redirect("account")

    return redirect("account")


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    un_read = profile.messages.filter(is_read=False).count()
    context = {"profile": profile, "un_read": un_read}

    if request.htmx:
        return render(request, "users/inbox.html#inbox-partial", context)

    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def message(request, pk):
    recipient = request.user.profile
    message = get_object_or_404(Message, id=pk, recipient=recipient)

    if not message.is_read:
        message.is_read = True
        message.save()

    context = {"message": message}

    if request.htmx:
        return render(request, "users/message.html#message-detail-partial", context)

    return render(request, "users/message.html", context)


@login_required(login_url="login")
def delete_message(request, pk):
    message = get_object_or_404(Message, id=pk, recipient=request.user.profile)

    if request.method == "POST":
        message.delete()
        messages.success(request, "Message deleted successfully!")
        return redirect("inbox")

    return redirect("inbox")


def send_message(request, pk):

    recipient = get_object_or_404(Profile, id=pk)
    message_form = MessageForm()

    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            msg = message_form.save(commit=False)
            if request.user.is_authenticated:
                msg.sender = request.user.profile
                msg.name = request.user.profile.name
                msg.email = request.user.profile.email
            msg.recipient = recipient
            msg.save()
            messages.success(request, 'Message sent successfully!')

            return redirect("profile_detail", pk=recipient.id)

        # Validation errors — re-render form partial
        if request.htmx:
            context = {"message_form": message_form, "recipient": recipient}
            return render(
                request, "users/send_message.html#send-message-partial", context
            )

    context = {"message_form": message_form, "recipient": recipient}

    if request.htmx:
        return render(request, "users/send_message.html#send-message-partial", context)

    return render(request, "users/send_message.html", context)


def unsubscribe(request, signature):
    signer = Signer()
    try:
        profile_id = signer.unsign(signature)
        profile = get_object_or_404(Profile, id=profile_id)
        profile.receive_notifications = False
        profile.save()
        messages.success(request, 'You have been successfully unsubscribed from email notifications.')
    except BadSignature:
        messages.error(request, 'Invalid or expired unsubscribe link.')
    
    return redirect('login')
