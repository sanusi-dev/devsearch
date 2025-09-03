from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from .utils import search_profiles
from projects.utils import pagination

def auth_view(request):

    if request.user.is_authenticated:
        return redirect('profile_list')

    current_url_name = request.resolver_match.url_name
    login_form = AuthenticationForm()
    register_form = UserRegistrationForm()

    if request.method == 'POST' and "login_submit" in request.POST:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            if request.GET.get('next'):
                prev_url = request.GET.get('next')
                return redirect(prev_url)
            else:
                return redirect('profile_list')

    if request.method == 'POST' and 'signup_submit' in request.POST:
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, f'Account created for {request.POST['username']}! Please log in.')

            return redirect('login')


    context = {
        'login_form': login_form,
        'register_form': register_form,
        'current_url_name': current_url_name
    }
    
    return render(request, 'users/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def profile_list(request):
    search_query, profiles = search_profiles(request)
    page_obj = pagination(request, profiles)

    context = {'page_obj': page_obj, 'search_query':search_query}
    return render (request, 'users/profile_list.html', context)

def profile_detail(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    return render (request, 'users/profile_detail.html', context)

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'users/user_account.html', context)

@login_required(login_url='login')
def profile_edit(request):
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('account')
        
    context = {'profile_form': profile_form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def create_skill(request):
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user.profile
            form.save()
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'users/skill_create.html', context)

@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)


    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'users/skill_create.html', context)

@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    
    context = {'skill': skill}
    return render(request, 'users/delete.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    un_read = profile.messages.filter(is_read=False).count()
    context = {'profile': profile, 'un_read': un_read}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def message(request, pk):
    print(request.resolver_match.url_name)
    recipient = request.user.profile
    message = get_object_or_404(Message, id=pk, recipient=recipient)

    if not message.is_read:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)


def send_message(request, pk):

    recipient = get_object_or_404(Profile, id=pk)
    message_form = MessageForm()

    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form = message_form.save(commit=False)
            if request.user.is_authenticated:
                message_form.sender = request.user.profile
                message_form.name = request.user.profile.name
                message_form.email = request.user.profile.email
            message_form.recipient = recipient
            message_form.save()
            return redirect('profile_detail', pk=recipient.id)
        else:
            message_form = MessageForm()
        

    context = {
        'message_form': message_form, 
        'recipient': recipient
    }

    return render(request, 'users/send_message.html', context)