import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from community.models import Review

User = get_user_model()


@csrf_exempt
@login_required
def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        user_profile = request.user.userprofile
        user_profile.avatar = request.FILES["avatar"]
        user_profile.save()

        return JsonResponse({}, status=200)

    return JsonResponse({}, status=400)


@csrf_exempt
@login_required
def update_user_info(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from request

            new_username = data.get("username", "").strip()
            new_email = data.get("email", "").strip()

            if not new_username or not new_email:
                return JsonResponse({}, status=400)

            # Ensure username is unique
            if (
                User.objects.exclude(id=request.user.id)
                .filter(username=new_username)
                .exists()
            ):
                return JsonResponse({}, status=400)

            # Ensure email is unique
            if (
                User.objects.exclude(id=request.user.id)
                .filter(email=new_email)
                .exists()
            ):
                return JsonResponse({}, status=400)

            # Update user info
            user = request.user
            user.username = new_username
            user.email = new_email
            user.save()

            return JsonResponse({}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({}, status=400)

    return JsonResponse({}, status=405)


@csrf_exempt
@login_required
def delete_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from request
            review_id = data.get("review_id")

            if not review_id:
                return JsonResponse({}, status=400)

            try:
                review = Review.objects.get(
                    id=review_id, user=request.user
                )  # Check ownership
                review.delete()
                return JsonResponse({}, status=200)
            except Review.DoesNotExist:
                return JsonResponse({}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({}, status=400)

    return JsonResponse({}, status=405)
