from django.contrib.auth.models import User
from django.db import models


# User Health Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    EXPERIENCE_CHOICES = [
        ("mental_relaxation", "راحة نفسية"),
        ("physical_recovery", "استشفاء جسدي"),
        ("physical_activity", "نشاط بدني"),
    ]
    experience_type = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)

    # Health conditions (Multiple selections)
    HEALTH_CHOICES = [
        ("stress", "Stress"),
        ("pain", "Pain"),
        ("sleep", "Sleep"),
        ("fatigue", "Fatigue"),
        ("digestive", "Digestive"),
        ("energy", "Energy"),
    ]
    health_conditions = models.CharField(max_length=50, choices=HEALTH_CHOICES)


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

    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    image = models.URLField(max_length=1000)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    experience_type = models.CharField(
        max_length=50, choices=UserProfile.EXPERIENCE_CHOICES
    )
    health_condition = models.CharField(
        max_length=50, choices=UserProfile.HEALTH_CHOICES
    )


class WellnessService(models.Model):
    place = models.OneToOneField(
        "WellnessPlace", on_delete=models.CASCADE, related_name="service"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(max_length=1000)
    more_info = models.TextField(blank=True, null=True)  # To store extra details

    def __str__(self):
        return self.title


class Booking(models.Model):
    SESSION_TYPE_CHOICES = [
        ("group", "جلسة جماعية"),
        ("private", "تجربة خاصة"),
        ("consultation", "استشارة مع أخصائي"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(
        WellnessService, on_delete=models.CASCADE, related_name="bookings"
    )
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title} ({self.session_type})"
