from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def landing_page(request):
    return render(request, "base/landing.html")


@login_required
def recommendations_page(request):
    return render(request, "base/recommendations.html")
