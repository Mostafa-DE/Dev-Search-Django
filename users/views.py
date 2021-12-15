from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginationProfiles



def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginationProfiles(request, profiles, 3)
    
    context={
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range
    }
    return render(request ,'users/profiles.html', context)



def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    skillsWithDesc = profile.skill_set.exclude(description__exact="")
    skillsWithoutDesc = profile.skill_set.filter(description="")
    context={
        "profile": profile,
        "skillsWithDesc":skillsWithDesc,
        "skillsWithoutDesc":skillsWithoutDesc
    }
    return render(request ,'users/user-profile.html', context)



def loginUser(request):
    page = "login"
    context = {
        "page": page
    }
    
    if request.user.is_authenticated:
        return redirect("profiles")
    
    if request.method == 'POST':
        username= request.POST['username'].lower()
        password= request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username does not exist")
            
        user = authenticate(request, username=username, password=password) 
        
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,"Username or password does not exist")
            
            
    return render(request, 'users/login_register.html', context)



def logoutUser(request):
    logout(request)
    messages.success(request,"User was successfully logged out")
    return redirect('login')



def registerUser(request):
    page="register"
    form = CustomUserCreationForm()
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # we put commit = False to create a instance from user to edit and login
            user.username = user.username.lower()
            user.save()
            
            messages.success(request,"User account was successfully created")
            
            login(request, user)
            return redirect("edit-account")
        
        else:
            messages.error(request,"Somthing went wrong during registration")

    
    context = {
        "page": page,
        "form": form
    }
    return render(request, 'users/login_register.html', context)



@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    allSkills = profile.skill_set.all()
    context = {
        "profile": profile,
        "allSkills":allSkills,
    }
    return render(request, 'users/account.html', context)
    
    

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return redirect("account")
    
    context = {
        "form": form
    }
    return render(request, 'users/profile_form.html', context)




@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit= False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill was created successfully")

            return redirect("account")
    
    context = {
        "form": form
    }
    return render(request, 'users/skill_form.html', context)




@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill was updated successfully")

            return redirect("account")
    
    context = {
        "form": form
    }
    return render(request, 'users/skill_form.html', context)



def deleteSkill(request, pk):
    
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request,"Skill was deleted successfully")
        return redirect("account")
    context = {
        "object": skill
    }
    return render(request, 'delete_confirm_template.html', context)



@login_required(login_url="login")
def userInbox(request):
    profile = request.user.profile # get user profile 
    profileMessages =  profile.messages.all() # get all user messages 
    unReadMessages = profileMessages.filter(is_read=False).count() # get all unread messages
    context = {
        "profileMessages": profileMessages,
        "unReadMessages": unReadMessages
    }
    return render(request, 'users/user_inbox.html', context)


@login_required(login_url="login")
def viewUserMessage(request, pk):
    profile = request.user.profile 
    message = profile.messages.get(id=pk)
    if message.is_read == False: # mark message as read
        message.is_read = True
        message.save()
    context = {
        "message": message
    }
    return render(request, 'users/user_message.html', context)



def createMessage(request, pk):
    receiver = Profile.objects.get(id=pk)
    form = MessageForm()
    
    try:
        sender = request.user.profile
    except:
        sender = None
        
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit= False)
            message.sender = sender
            message.receiver = receiver
            
            if sender:
                message.name = sender.name
                message.email = sender.email
                
            message.save()
            messages.success(request, "Your message was successfully sent!!")
            return redirect('user-profile', pk=receiver.id)
            
    
    context = {
        "receiver": receiver,
        "form": form
    }
    return render(request, 'users/message_form.html', context)
