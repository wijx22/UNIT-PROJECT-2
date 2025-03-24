from django.urls import path

from .views import get_recommendations, landing_page, recommendations_page,destinations_page

urlpatterns = [
    path("", landing_page, name="landing"),
    path("recommendations", recommendations_page, name="recommendations"),
    path("api/recommendations", get_recommendations, name="recommendations_api"),
    path("destinations",  destinations_page, name="destinations"),
]
