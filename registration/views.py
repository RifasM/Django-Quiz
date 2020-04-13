from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from registration.models import Register


# Create your views here.
from registration.forms import SignUpForm, SignInForm

from quiz.views import test_name


def login(request):
    try:
        if request.method == 'POST':

            username = request.POST["username"]
            raw_password = request.POST["password"]
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return render(request, 'dashboard.html', {"user": request.user.get_full_name(), "test_name": test_name})
        else:
            form = SignInForm()
        return render(request, 'signin.html', {'form': form, "invalid": False})
    except Exception as e:
        form = SignInForm()
        return render(request, 'signin.html', {'form': form, "invalid": True})


def signup(request):
    try:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                usn = form.cleaned_data.get('usn')
                name = form.cleaned_data.get('first_name')
                Register.objects.create(name=name, usn=usn, pk=username)
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                User.objects.filter(username=username).update(email=username)
                return render(request, 'dashboard.html', {"user": request.user.get_full_name(), "test_name": test_name})
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    except Exception as e:
        return render(request, "error.html", {"user": "Anonymous Panda"})


def logout_user(request):
    try:
        logout(request)
        form = SignInForm
        return render(request, 'signin.html', {'form': form})
    except Exception as e:
        return render(request, "error.html", {"user": "Anonymous Panda"})