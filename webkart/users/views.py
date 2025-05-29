from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm



# Create your views here.

# register
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request, form.save())       # login after registration
            # return redirect("index")
            return redirect("users:login")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

# login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("index")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


# logout
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:login")