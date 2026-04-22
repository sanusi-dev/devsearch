from .models import Profile
from django.db.models import Q



def search_profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    profiles = Profile.objects.prefetch_related('skill_set').filter(Q(name__icontains=search_query) | 
                                      Q(short_intro__icontains=search_query) |
                                      Q(skill__name__icontains=search_query)).distinct()
    
    return search_query, profiles