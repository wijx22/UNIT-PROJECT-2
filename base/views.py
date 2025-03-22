from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


def landing_page(request: HttpRequest):
    return render(request, "base/landing.html")


@login_required
def recommendations_page(request: HttpRequest):
    return render(request, "base/recommendations.html")
