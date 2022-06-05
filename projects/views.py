from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm,ReviewForm
from .utils import searchProjects,paginateProjects
from django.contrib import messages as m
# from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage


# Create your views here.
def projects(request): 
    obj, search_query = searchProjects(request)
    custom_range, obj = paginateProjects(request, obj,6)
        
    return render(request, 'projects/projects.html', {
        'obj': obj,
        'search_query': search_query,
        'custom_range':custom_range,
    })


def project(request, pk):
    obj1 = Project.objects.get(id=pk)
    
    form  = ReviewForm()
    
    if request.method == "POST":
        form  = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = obj1
        review.owner = request.user.profile
        review.save()
        # Update vote count
        # Update vote count
        obj1.getVoteCount
        m.success(request, "Review successfully submitted")
        return redirect('project', pk=obj1.id)     

    tag = obj1.tags.all()

    return render(request, 'projects/single_project.html', {
        'obj1': obj1,
        'tag': tag,
        'form': form,
        
    })

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        print(request.POST)
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    return render(request, 'projects/project_form.html', {
        'form': form,
    })

@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    # proj = Project.objects.get(id=pk)
    proj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=proj)

    if request.method == "POST":
        print(request.POST)
        form = ProjectForm(request.POST, request.FILES, instance=proj)

        if form.is_valid():
            form.save()
            return redirect('account')

    return render(request, 'projects/project_form.html', {
        'form': form,
    })

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
   
    pro = profile.project_set.get(id=pk)
    # pro = Project.objects.get(pk=pk)

    if request.method == "POST":
        pro.delete()
        return redirect('account')

    return render(request, 'delete-template.html', {
        'object': pro,

    })
