import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.models import WellnessPlace

from .forms import ReplyForm, ReviewForm
from .models import Reply, Review, ReviewLike


def community_reviews(request: HttpRequest):
    reviews = Review.objects.filter(status="approved").order_by("-created_at")
    data = []

    for review in reviews:
        replies = Reply.objects.filter(review=review)
        data.append(
            {
                "id": review.id,
                "userId": review.user.id,
                "userName": review.user.username,
                "userAvatar": review.user.userprofile.avatar.url,
                "placeId": review.wellness_place.id,
                "placeName": review.wellness_place.name,
                "rating": review.rating,
                "text": review.comment,
                "timestamp": review.created_at,
                "likes": review.likes_count(),
                "liked": ReviewLike.objects.filter(
                    user=request.user, review=review
                ).exists(),  # Modify this based on the user's likes
                "replies": [
                    {
                        "id": reply.id,
                        "userId": reply.user.id,
                        "userName": reply.user.username,
                        "userAvatar": reply.user.userprofile.avatar.url,
                        "text": reply.text,
                        "timestamp": reply.created_at,
                    }
                    for reply in replies
                ],
            }
        )

    return JsonResponse(data, safe=False)


def places_list(request: HttpRequest):
    lang = request.GET.get("lang", "en")
    places = WellnessPlace.objects.filter(language=lang).values("id", "name")
    return JsonResponse(list(places), safe=False)


@csrf_exempt
@login_required
def add_review(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        form = ReviewForm(data)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return JsonResponse(
                {"message": "Review added successfully", "reviewId": review.id},
                status=201,
            )

        return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@login_required
def add_reply(request: HttpRequest, id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return JsonResponse({"error": "Review not found"}, status=404)

        form = ReplyForm(data)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.user = request.user
            reply.save()
            return JsonResponse(
                {"message": "Reply added successfully", "replyId": reply.id}, status=201
            )

        return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@login_required
def like_review(request: HttpRequest, id):
    if request.method == "POST":
        try:
            review = Review.objects.get(id=id)
            review_likes = ReviewLike.objects.filter(user=request.user, review=review)
            if review_likes.exists():
                review_likes.delete()
            else:
                ReviewLike.objects.create(user=request.user, review=review)

            return JsonResponse(
                {"message": "Review liked successfully"},
                status=200,
            )
        except Review.DoesNotExist:
            return JsonResponse({"error": "Review not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)
