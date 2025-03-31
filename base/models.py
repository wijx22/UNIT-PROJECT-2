from django.conf import settings
from django.core.validators import RegexValidator, URLValidator
from django.db import models


# User Health Profile
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="avatars/%y/%m/%d",
        default="images/default-avatar.jpg",
        null=True,
        blank=True,
    )
    EXPERIENCE_CHOICES = [
        ("mental_relaxation", "راحة نفسية"),
        ("physical_recovery", "استشفاء جسدي"),
        ("physical_activity", "نشاط بدني"),
    ]

    # Health conditions (Multiple selections)
    HEALTH_CHOICES = [
        ("stress", "Stress"),
        ("pain", "Pain"),
        ("sleep", "Sleep"),
        ("fatigue", "Fatigue"),
        ("digestive", "Digestive"),
        ("energy", "Energy"),
    ]


# Wellness Places (Real-world places for recommendations)
class WellnessPlace(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("ar", "Arabic"),
    ]
    LOCATION_CHOICES = [
        ("riyadh", "Riyadh"),
        ("aseer", "Aseer"),
        ("jeddah", "Jeddah"),
        ("alula", "Alula"),
        ("taif", "Taif"),
        ("al-baha", "Al baha"),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name="Place Name",
        help_text="The name of the wellness place.",
    )
    description = models.TextField(
        verbose_name="Place Description",
        help_text="A detailed description of the wellness place.",
    )
    content = models.TextField(
        verbose_name="Place Content",
        help_text="HTML content providing a detailed description of the wellness place.",
        default="",
    )
    location = models.CharField(
        max_length=50,
        choices=LOCATION_CHOICES,
        verbose_name="Location",
        help_text="The location of the wellness place.",
    )
    image = models.URLField(
        max_length=1000,
        verbose_name="Place Image URL",
        help_text="A URL pointing to an image representing the wellness place.",
        validators=[URLValidator()],
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="en",
        verbose_name="Language",
        help_text="The primary language used at the wellness place.",
    )
    experience_type = models.CharField(
        max_length=50,
        choices=UserProfile.EXPERIENCE_CHOICES,
        verbose_name="Experience Type",
        help_text="The type of experience offered at the wellness place.",
    )
    health_condition = models.CharField(
        max_length=50,
        choices=UserProfile.HEALTH_CHOICES,
        verbose_name="Health Condition",
        help_text="The health condition supported by the wellness place.",
    )

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def __str__(self):
        return self.name


class WellnessPlaceLike(models.Model):
    place = models.ForeignKey(
        WellnessPlace, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class WellnessService(models.Model):
    DURATION_CHOICES = [
        (30, "30 minutes"),
        (60, "60 minutes"),
        (90, "90 minutes"),
        (120, "120 minutes"),
    ]

    GROUP_SIZE_CHOICES = [
        (1, "Solo"),
        (2, "2-4 people"),
        (5, "5-8 people"),
        (9, "More than 8"),
    ]

    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("ar", "Arabic"),
        ("both", "English & Arabic"),
    ]

    AVAILABILITY_CHOICES = [
        ("daily", "Daily"),
        ("weekends", "Weekends"),
        ("weekdays", "Weekdays"),
    ]

    place = models.OneToOneField(
        "WellnessPlace",
        on_delete=models.CASCADE,
        related_name="service",
        verbose_name="Wellness Place",
        help_text="The wellness place associated with this service.",
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Service Title",
        help_text="The title of the wellness service.",
    )
    description = models.TextField(
        verbose_name="Service Description",
        help_text="A detailed description of the wellness service.",
    )
    image = models.URLField(
        max_length=1000,
        verbose_name="Service Image URL",
        help_text="A URL pointing to an image representing the service.",
        validators=[URLValidator()],
    )
    language = models.CharField(
        max_length=4,
        choices=LANGUAGE_CHOICES,
        default="both",
        verbose_name="Language",
        help_text="The primary language used at the wellness service.",
    )

    duration = models.IntegerField(choices=DURATION_CHOICES, default=90)
    group_size = models.IntegerField(choices=GROUP_SIZE_CHOICES, default=2)
    availability = models.CharField(
        max_length=10, choices=AVAILABILITY_CHOICES, default="daily"
    )

    def __str__(self):
        return self.title


class WhatToExpect(models.Model):
    wellness_place = models.ForeignKey(
        WellnessService, on_delete=models.CASCADE, related_name="expectations"
    )
    description = models.TextField()

    def __str__(self):
        return f"Expectation for {self.wellness_place.name}"


import random
import string


def generate_booking_reference():
    """Generate a random 14-character booking reference with uppercase letters and numbers."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=14))


class Booking(models.Model):
    SESSION_TYPE_CHOICES = [
        ("group", "جلسة جماعية"),
        ("private", "تجربة خاصة"),
        ("consultation", "استشارة مع أخصائي"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="User",
        help_text="The user who made the booking.",
    )
    service = models.ForeignKey(
        WellnessService,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Service",
        help_text="The wellness service being booked.",
    )
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        verbose_name="Session Type",
        help_text="Type of session being booked.",
    )
    booking_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Booking Date",
        help_text="The date and time when the booking was created.",
    )

    # Additional user info
    full_name = models.CharField(
        max_length=255,
        default="",
        verbose_name="Full Name",
        help_text="The full name of the user making the booking.",
    )
    phone_number = models.CharField(
        max_length=20,
        default="",
        verbose_name="Phone Number",
        help_text="The phone number of the user.",
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    preferred_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Preferred Date",
        help_text="The preferred date for the session.",
    )  # Default to allow empty
    preferred_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Preferred Time",
        help_text="The preferred time for the session.",
    )  # Default to allow empty
    additional_notes = models.TextField(
        blank=True,
        null=True,
        default="",
        verbose_name="Additional Notes",
        help_text="Any additional notes or details provided by the user.",
    )  # Extra details from the user
    booking_reference = models.CharField(
        max_length=14, unique=True, default=generate_booking_reference
    )

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"
