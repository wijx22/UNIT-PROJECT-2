import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import WellnessPlace


def landing_page(request: HttpRequest):
    return render(request, "base/landing.html")


@login_required
def recommendations_page(request: HttpRequest):
    return render(request, "base/recommendations.html")


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def get_recommendations(request: HttpRequest):
    data = json.loads(request.body)
    try:
        recommendations = WellnessPlace.objects.filter(
            experience_type=data.get("experience_type"),
            health_condition__in=data.get("health_conditions"),
            language=data.get("language"),
        ).distinct()

        # Format response data
        data = [
            {
                "id": place.id,
                "name": place.name,
                "description": place.description,
                "image": place.image,
                "location": place.location,
                "experience_type": place.experience_type,
            }
            for place in recommendations
        ]

        return JsonResponse({"status": "success", "recommendations": data}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
