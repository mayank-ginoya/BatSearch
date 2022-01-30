from email import message
from multiprocessing import context
from xml.etree.ElementPath import prepare_parent
from django.shortcuts import render , redirect
from django.contrib.auth import login , authenticate ,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .utils import searchProfiles,paginationProfiles

# from django.contrib.auth.forms import UserCreationForm
from .models import Message, Profile , User , Skill , Message
from .forms import CustomUserCreation, ProfileForm , SkillForm , MessageForm


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username Doesn't Exist")
        
        user = authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,'Username or Password is Incorrect')

    return render(request,'users/login_register.html')

def logoutPage(request):
    logout(request)
    messages.success(request,"Username Successfully Logged Out !")
    return redirect('login')

def registerPage(request):
    page = 'register'
    form = CustomUserCreation()

    if request.method == "POST":
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,"User account was Created")
            login(request,user)
            return redirect('edit-account')
        
        else:
            messages.error(request,"An Error Has Occured")

    context ={'page':page , 'form' : form}
    return render(request,'users/login_register.html',context)

# Create your views here.   
def profiles(request):
    profiles,search_query = searchProfiles(request)

    custom_range , profiles = paginationProfiles(request,profiles)
    context = {'profiles':profiles , 'search_query':search_query , 'custom_range':custom_range}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile':profile , 'topSkills':topSkills , 'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    projects = profile.project_set.all()
    context = {'profile':profile , 'topSkills':topSkills , 'otherSkills':otherSkills ,'projects':projects}
    return render(request,'users/account.html',context)

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        try:
            if form.is_valid():
                form.save()
                return redirect('account')
        except :
                messages.error(request,"An Error Has Occured")

    context = {'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,f"{skill.name} Skill was added to {profile.name}")
            return redirect('account')
        else:
            messages.error(request,f"{profile} already have {form.name}")
            return redirect('account')

    context ={'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance = skill)

    if request.method == 'POST':
        form = SkillForm(request.POST , instance= skill)
        if form.is_valid():
            form.save()
            messages.success(request,f"{skill} Skill was updated")
            return redirect('account')

    context ={'form':form}
    return render(request,'users/skill_form.html',context)

@login_required
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method=="POST":
        skill.delete()
        messages.success(request,f"{skill} Skill was Succesfully Deleted")
        return redirect('account')
    context = {'object':skill,'profile':profile}
    return render(request,'delete_template.html',context)

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequest':messageRequests , 'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url="login")
def viewMessage(request,pk):
    profile = request.user.profile
    messageReq = profile.messages.get(id=pk)
    if messageReq.is_read==False:
        messageReq.is_read = True
        messageReq.save()
    context ={'messageReq':messageReq}
    return render(request,'users/message.html',context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method =="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request,f"Message Sent Successfully to {recipient.name}")
            return redirect('user-profile',pk=recipient.id)
    context = {'recipient':recipient , 'form':form}
    return render(request,'users/message_form.html',context)