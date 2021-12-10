from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

def homePage(request):
    projects = Project.objects.all()
    context = {
        "projects": projects
    }
    return render(request, 'projects/home.html', context)



def projects(request, pk):
    projectObj = Project.objects.get(id=pk)
    
    return render(request, 'projects/single-project.html', { "projects": projectObj})



@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile # current logged in user
    form = ProjectForm()
    
    if(request.method == 'POST'):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False) # give us the instance to the current project
            project.owner = profile
            project.save()
            return redirect("home")
    
    context = {"form": form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile # get the logged in user profile
    project = profile.project_set.get(id=pk) # get project that own to logged in user for update it
    form = ProjectForm(instance=project)
    if(request.method == 'POST'):
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")
    
    context = {"form": form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile # get the logged in user profile
    project = profile.project_set.get(id=pk) # get that specific project that own to logged in user and delete it 
    if(request.method == 'POST'):
        project.delete()
        return redirect("account")
    context ={"object": project}
    return render(request, 'delete_confirm_template.html', context)