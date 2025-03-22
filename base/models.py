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
        ("stress", "التوتر والقلق"),
        ("muscle_pain", "آلام العضلات والمفاصل"),
        ("sleep_issues", "مشاكل النوم"),
        ("chronic_fatigue", "التعب والإرهاق المزمن"),
    ]
    health_conditions = models.ManyToManyField("HealthCondition")


class HealthCondition(models.Model):
    name = models.CharField(max_length=100)


# Wellness Places (Real-world places for recommendations)
class WellnessPlace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.URLField(max_length=1000)
    experience_type = models.CharField(
        max_length=50, choices=UserProfile.EXPERIENCE_CHOICES
    )
    health_conditions = models.ManyToManyField(HealthCondition)


# Recommendations
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(WellnessPlace, on_delete=models.CASCADE)
    recommended_on = models.DateTimeField(auto_now_add=True)
