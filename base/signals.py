import json
import random

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import WellnessPlace, WellnessService

# Load dummy data once
with open("base/data/dummy-services.json", "r", encoding="utf-8") as f:
    DUMMY_SERVICES = json.load(f)


def get_random_service_data(language):
    lang_key = "ar" if language == "ar" else "en"
    return random.choice(DUMMY_SERVICES[lang_key])


def fetch_random_image(query):
    headers = {"Authorization": settings.PEXELS_API_KEY}
    params = {"query": query, "per_page": 15}
    try:
        response = requests.get(
            "https://api.pexels.com/v1/search", headers=headers, params=params
        )
        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            # Filter only landscape photos (optional)
            landscape_photos = [
                photo for photo in photos if photo.get("src", {}).get("landscape")
            ]
            if landscape_photos:
                image_url = random.choice(landscape_photos)["src"]["landscape"]
                return image_url
    except Exception as e:
        print(f"Error fetching image: {e}")

    # Fallback image (landscape placeholder)
    return "https://images.pexels.com/photos/6959775/pexels-photo-6959775.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200"


@receiver(post_save, sender=WellnessPlace)
def create_wellness_service(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, "service"):
            service_data = get_random_service_data(instance.language)
            image_url = fetch_random_image(service_data["title"])

            WellnessService.objects.create(
                place=instance,
                title=service_data["title"],
                description=service_data["description"],
                more_info=service_data.get("more_info", ""),
                image=image_url,
            )
