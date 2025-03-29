from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def community_reviews(request):

    return render(
        request,
        "community/community-reviews.html",
    )
