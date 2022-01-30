from .models import Profile , Skill 
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginationProfiles(request,profiles):
    
    page = request.GET.get('page')
    results=6
    paginator = Paginator(profiles,results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    leftIndex = (int(page)-2) 
    if leftIndex<1:
        leftIndex=1
    rightIndex = (int(page)+2) 
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages

    custom_range = range(leftIndex,rightIndex)  
    return custom_range,profiles

def searchProfiles(request):
    search_query =''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')   
    print('SEARCH: ',search_query)
    skills = Skill.objects.filter(name__iexact=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills))
    print(profiles)
    return profiles.order_by('name'),search_query
