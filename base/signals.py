import json
import random

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Booking, WellnessPlace, WellnessService

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


@receiver(post_save, sender=Booking)
def send_booking_confirmation_email(sender, instance, created, **kwargs):
    if created:
        # Extract booking details
        user_email = instance.user.email
        subject = "Booking Confirmation - Your Wellness Experience"
        service_title = instance.service.title
        place_name = instance.service.place.name
        session_type = instance.get_session_type_display()
        booking_reference = instance.booking_reference
        booking_date = instance.booking_date.strftime("%Y-%m-%d %H:%M:%S")
        preferred_date = (
            instance.preferred_date.strftime("%Y-%m-%d")
            if instance.preferred_date
            else "Not specified"
        )
        preferred_time = (
            instance.preferred_time.strftime("%H:%M:%S")
            if instance.preferred_time
            else "Not specified"
        )
        phone_number = instance.phone_number
        additional_notes = instance.additional_notes or "No additional notes"

        # Render email template
        context = {
            "full_name": instance.full_name,
            "service_title": service_title,
            "place_name": place_name,
            "session_type": session_type,
            "booking_reference": booking_reference,
            "booking_date": booking_date,
            "preferred_date": preferred_date,
            "preferred_time": preferred_time,
            "phone_number": phone_number,
            "additional_notes": additional_notes,
        }

        html_message = render_to_string("emails/booking_confirmation.html", context)
        plain_message = strip_tags(html_message)  # Convert HTML to plain text

        # Send email
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
