from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm


def signup_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('recommendations')
    
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect(
                "recommendations"
            )  # Change "home" to your desired redirect page
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('recommendations')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(
                    "recommendations"
                )  # Change "home" to your desired redirect page
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
