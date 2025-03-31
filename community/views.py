from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from base.models import UserProfile


@login_required
def community_reviews(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(
        request, "community/community-reviews.html", {"user_profile": user_profile}
    )
