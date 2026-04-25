from .models import Project
from django.db.models import Q
from django.core.paginator import Paginator


def search_projects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    projects = Project.objects.select_related('owner').prefetch_related('tags').filter(Q(title__icontains=search_query) |
                                      Q(owner__name__icontains=search_query) |
                                      Q(tags__name__icontains=search_query) |
                                      Q(description__icontains=search_query)
    ).distinct()

    return search_query, projects


def pagination(request, query):
    
    query = query.order_by('-created_at')
    page_number = request.GET.get('page')
    items_per_page = 9
    paginator = Paginator(query, items_per_page)
    page_obj = paginator.get_page(page_number)

    return page_obj