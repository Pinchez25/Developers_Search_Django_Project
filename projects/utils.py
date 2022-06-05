from django.db.models import Q
from .models import Project,Tag
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):
    
    page = request.GET.get('page')
    # results = 3
    # 3 results per page
    paginator = Paginator(projects, results)
    
    try:
       projects = paginator.page(page)
    except (PageNotAnInteger, Exception):
        # return HttpResponse(f"Error: {e}")
        page=1
        projects = paginator.page(page)
        
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    """
       If we have a many pages to render using the pagination, we could have an
      ugly display of pagination tags. Django doesn't provide a better way to solve this
       eg. if you are in the first page (page 1), show the next 5 tags andif you arein the 5th 
       page show the previous 2 and next say 3. This is just a scenario. For this we'll create our
       own pagination.
    """  
    leftIndex = (int(page) - 4)
    
    if leftIndex < 1:
        leftIndex = 1
        
    rightIndex = (int(page) + 5)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex,rightIndex)
        
    
    return custom_range, projects
    

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    tags = Tag.objects.filter(name__icontains=search_query)
        
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)|
        Q(description__icontains=search_query)|
        Q(owner__name__icontains=search_query)|
        Q(tags__in=tags)
    )
    
    return projects, search_query