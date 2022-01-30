from turtle import left
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q
from django.contrib import messages

from projects.utils import paginationProjects, searchProjects


from .models import Project,Tag
from .forms import ProjectForm , ReviewForm


def projects(request):
    # projects = Project.objects.order_by('name')
    # projects = Project.objects.all()
    # projects = searchProjects(request).order_by('name')
    # print(projects)
    # if search_query!='':
    #     messages.success(request,f"Results of {search_query}")
    projects,search_query = searchProjects(request)
    custom_range,projects  =  paginationProjects(request,projects)
    context = {'projects':projects,'custom_range':custom_range , 'search_query':search_query}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    # print(projectObj)
    form = ReviewForm()

    if request.method =="POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request , f"Your Review was succesfully submitted")
        return redirect('project',pk=projectObj.id)

        # Update Project Cote Count


    return render(request,'projects/single-project.html',{'project':projectObj ,'form':form })

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        newtags = request.POST.get("newtags").replace(',' , ' ').split()
        #print(request.POST)
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        newtags = request.POST.get("newtags").replace(',' , ' ').split()
        for tag in newtags:
            tag,created = Tag.objects.get_or_create(name=tag)
            project.tags.add(tag)

        form = ProjectForm(request.POST , request.FILES , instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form , 'project':project}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method =="POST":
        project.delete()
        return redirect('account')
    context = {'object':project , 'profile':profile}
    return render(request,'delete_template.html',context)
