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


# Recommendations
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(WellnessPlace, on_delete=models.CASCADE)
    recommended_on = models.DateTimeField(auto_now_add=True)
