from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm, LoginForm
from django.contrib.auth import login
from .models import Profile
#from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def register(request):
    if request.method == 'POST':
     form = CreateUserForm(request.POST)
     if form.is_valid():
         form.save()
         return redirect('user-login')
    else:
        form = CreateUserForm()

    return render(request, 'user/register.html', {'form': form})


def Profile_view(request):
    profile = Profile.objects.all()
    context = {'profile': profile}
    return render(request, 'user/profile.html', context)


def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
           user_form.save()
           profile_form.save()
        return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,

    }
    return render(request, 'user/profile_update.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pharma-index')  # Replace 'home' with the appropriate URL name
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'user/login.html', context)
