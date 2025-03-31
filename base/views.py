import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import BookingForm
from .models import WellnessPlace, WellnessPlaceLike, WellnessService


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
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
def destinations_page(request: HttpRequest):
    locations = ["riyadh", "aseer", "jeddah", "alula", "taif", "al-baha"]
    destinations = {}

    for location in locations:
        arabic_places = WellnessPlace.objects.filter(
            location=location,
            language="ar",
        )[:5]
        english_places = WellnessPlace.objects.filter(
            location=location,
            language="en",
        )[:5]

        # Matching Arabic and English records by ID (assuming same order)
        places = []
        for ar, en in zip(arabic_places, english_places):
            places.append({"ar": ar, "en": en})

        destinations[location] = places

    return render(request, "base/destinations.html", {"destinations": destinations})


def location_detail_view(request, location):
    # Get all places for this location in both languages
    arabic_places = WellnessPlace.objects.filter(location=location, language="ar")
    english_places = WellnessPlace.objects.filter(location=location, language="en")

    # Combine Arabic & English places together
    places = []
    for ar, en in zip(arabic_places, english_places):
        places.append({"ar": ar, "en": en})

    return render(
        request, "base/location-details.html", {"places": places, "location": location}
    )


@login_required
def booking_page(request, service_id, place_id):
    service = get_object_or_404(WellnessService, id=service_id)
    place = get_object_or_404(WellnessPlace, id=place_id)

    form = BookingForm()
    return render(
        request, "base/booking.html", {"form": form, "service": service, "place": place}
    )


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def booking_api(request):
    try:
        data = json.loads(request.body)
        form = BookingForm(data)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = get_object_or_404(
                WellnessService, id=data.get("service_id")
            )
            booking.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Booking successful!",
                    "booking_reference": booking.booking_reference,
                },
                status=201,
            )
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


def place_details(request, location, place_id):
    place = get_object_or_404(WellnessPlace, id=place_id)
    is_liked_place = WellnessPlaceLike.objects.filter(
        user=request.user, place=place
    ).exists()
    context = {"place": place, "location": location, "is_liked_place": is_liked_place}

    return render(request, "base/place-details.html", context)


def set_language(request):
    lang_code = request.GET.get(
        "lang", "en"
    )  # Default to 'en' if no language is provided
    response = JsonResponse({"message": f"Language set to {lang_code}"})
    response.set_cookie(
        "currentLang", lang_code, max_age=30 * 24 * 3600
    )  # Set cookie for 30 days
    return response


@csrf_exempt
@login_required
def like_place(request: HttpRequest, id):
    if request.method == "POST":
        try:
            place = WellnessPlace.objects.get(id=id)
            place_likes = WellnessPlaceLike.objects.filter(
                user=request.user, place=place
            )
            if place_likes.exists():
                place_likes.delete()
            else:
                WellnessPlaceLike.objects.create(user=request.user, place=place)

            return JsonResponse(
                {"message": "place liked successfully"},
                status=200,
            )
        except WellnessPlace.DoesNotExist:
            return JsonResponse({"error": "place not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)
