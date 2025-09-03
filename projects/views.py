from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .utils import search_projects, pagination


def project_list(request):
    search_query, projects = search_projects(request)
    page_obj = pagination(request, projects)

    context = {'search_query': search_query, 'page_obj': page_obj}
    return render(request, 'projects/project_list.html', context)

def project_detail(request, pk):
    project = Project.objects.get(id=pk)
    review_form = ReviewForm()
    reviewers = project.review_set.all().values_list('owner__id', flat=True)

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form = review_form.save(commit=False)
            review_form.owner = request.user.profile
            review_form.project = project
            review_form.save()
            return redirect('project_detail', pk=project.id)
    
    context = {'project': project, 'review_form': review_form, 'reviewers': reviewers}
    return render(request, 'projects/project_detail.html', context)

@login_required(login_url='login')
def project_create(request):
    form = ProjectForm
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user.profile
            form.save()
            return redirect('project_list')
        
    context = {'form': form}
    return render(request, 'projects/project_create.html', context)

@login_required(login_url='login')
def update_project(request, pk):

    project = Project.objects.get(id=pk)

    if project.owner != request.user:
        return redirect('profile_list')
    
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
        
    context = {'form': form}
    return render(request, 'projects/project_create.html', context)

@login_required(login_url='login')
def delete_project(request, pk):
    project = Project.objects.get(id=pk)

    if project.owner != request.user:
        return redirect('profile_list')
    
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
        
    return render(request, 'projects/delete.html', {'project': project})