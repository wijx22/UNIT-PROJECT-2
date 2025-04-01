from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from base.models import Booking, UserProfile, WellnessPlace, WellnessPlaceLike
from community.models import Review

from .forms import LoginForm, SignupForm


@login_required
def user_profile(request: HttpRequest):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    reviews = Review.objects.filter(user=request.user).order_by("-created_at")
    bookings = Booking.objects.filter(user=request.user).order_by("-booking_date")
    liked_places = WellnessPlaceLike.objects.filter(user=request.user)
    favorite_places = WellnessPlace.objects.filter(
        id__in=[liked_place.place.id for liked_place in liked_places]
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "reviews": reviews,
            "bookings": bookings,
            "favorite_places": favorite_places,
        },
    )


def signup_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("community_reviews")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("community_reviews")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("community_reviews")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("community_reviews")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
