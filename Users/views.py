from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles


# Create your views here.


def profiles(request):
    # search_query = ''

    # if request.GET.get('search_query'):
    #     search_query = request.GET.get('search_query')

    # print("SEARCH: ",search_query)

    # skills = Skill.objects.filter(name__iexact=search_query)

    # prof = Profile.objects.distinct().filter(Q(name__icontains=search_query)|
    #                               Q(short_intro__icontains=search_query)|
    #                               Q(skill__in = skills)

    #                               )
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    return render(request, 'Users/profiles.html', {
        'prof': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
    })


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # Skills with description
    topSkills = profile.skill_set.exclude(description__exact="")

    # Skills without description
    otherSkills = profile.skill_set.filter(description="")

    return render(request, 'Users/user-profile.html', {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
    })


def loginUser(request):
    page = 'login'
    # If user is logged in don't show the login page
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == "POST":
        # print(request.POST)
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            messages.error(request, "Username does not exist")
            print('Username does not exist')
        """
          authenticate method takes the credentials - in this case username and password -
          and makes sure the password matches the username and returns either the user instance or
          none.
        """
        user = authenticate(request, username=username, password=password)
        """
           if such user exists in the db i.e. the authenticate method returned user instance
           create a user session in the database and also get the session and add it to the browser
           cookies and login the user using the login function.
        """
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "Username or password is incorrect")
            print('Username or password is incorrect')

    return render(request, 'Users/login_register.html', {
        'page': page,
    })


def logoutUser(request):
    logout(request)
    messages.info(request, "User logged out")
    return redirect('login')


# def registerUser(request):
#     page='register'
#     form = UserCreationForm()
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save() 

#             messages.success(request,"User created successfully")
#             login(request,user)
#             return redirect('profiles')
#         else:
#             messages.error(request,"Error occurred during registration")

#     return render(request, 'Users/login_register.html',{
#         'page':page,
#         'form':form,
#     })

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User created successfully")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "Error occurred during registration")

    return render(request, 'Users/login_register.html', {
        'page': page,
        'form': form,
    })


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    # otherSkills = profile.skill_set.filter(description="")
    projects = profile.project_set.all()

    print(profile, " ", request.user)
    return render(request, 'Users/account.html', {
        'profile': profile,
        'skills': skills,
        'projects': projects,

    })


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect('account')

    return render(request, 'Users/profile_form.html', {
        'form': form,
    })


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill created successfully")
            return redirect('account')
    return render(request, 'Users/skill_form.html', {
        'form': form,
    })


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully")
            return redirect('account')
    return render(request, 'Users/skill_form.html', {
        'form': form,
    })


@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully")
        return redirect('account')
    return render(request, 'delete-template.html', {
        'object': skill,
    })

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    return render(request, 'Users/inbox.html', {
        'messageRequests':messageRequests,
        'unreadCount':unreadCount,

    })
@login_required(login_url="login")
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request,'Users/message.html',{
        'profile':profile,
        'message':message,
    })
    
def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
        
    if request.method == "POST":
        form = MessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
                
            message.save()
            messages.success(request,"Your message was successfully sent")
            return redirect('user-profile', pk=recipient.id)
    return render(request, 'Users/message_form.html',{
        'form':form, 
        'recipient':recipient,   
                                                      
    })