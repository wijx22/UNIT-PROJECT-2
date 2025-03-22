from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .models import Recommendation, UserProfile, WellnessPlace


def landing_page(request: HttpRequest):
    return render(request, "base/landing.html")


@login_required
def recommendations_page(request: HttpRequest):
    return render(request, "base/recommendations.html")


@login_required
def get_recommendations(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_experience = user_profile.experience_type
        user_health_conditions = user_profile.health_conditions.all()

        # Filter places that match the experience type and health conditions
        recommendations = WellnessPlace.objects.filter(
            experience_type=user_experience,
            health_conditions__in=user_health_conditions
        ).distinct()

        # Save recommendations
        Recommendation.objects.bulk_create([
            Recommendation(user=request.user, place=place)
            for place in recommendations
        ])

        # Format response data
        data = [
            {
                "id": place.id,
                "name": place.name,
                "description": place.description,
                "image": place.image,
                "location": place.location,
                "experience_type": place.experience_type
            }
            for place in recommendations
        ]

        return JsonResponse({"status": "success", "recommendations": data}, status=200)

    except UserProfile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User profile not found"}, status=404)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
