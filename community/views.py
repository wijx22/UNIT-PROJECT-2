from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from base.models import UserProfile


@login_required
def community_reviews(request):
    user_profile,_ = UserProfile.objects.get_or_create(user=request.user)
    return render(
        request, "community/community-reviews.html", {"user_profile": user_profile}
    )
