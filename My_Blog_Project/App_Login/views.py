from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.forms import SignUpForm, UserProfileChange, ProfilePic


# Create your views here.

# to create a user 
def sign_up(request):
    form = SignUpForm()
    registered = False
    
    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
            
    diction = {"form": form, "registered": registered}
    return render(request, "App_Login/signup.html", context=diction)


# login to the registered user account
def login_page(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    return render(request, "App_Login/login.html", context={"form":form})


# logout of an registered and logged in user
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:signin'))


# profile of a user
@login_required
def profile(request):
    return render(request, "App_Login/profile.html", context={})


# user details changing form
@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == "POST":
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
    return render(request, 'App_Login/change_profile.html', context={"form":form})



@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
            return HttpResponseRedirect(reverse('App_Login:profile'))
    diction = {"form":form, "changed": changed}
    return render(request, "App_Login/pass_change.html", context=diction)


@login_required
def add_pro_pic(request):
    form = ProfilePic()
    if request.method == "POST":
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
        
    return render(request, "App_Login/pro_pic_add.html", context={"form": form})


@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == "POST":
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("App_Login:profile"))
    return render(request, "App_Login/pro_pic_add.html", context={"form": form})
        




