from django.urls import path

from .views import (
    destinations_page,
    get_recommendations,
    landing_page,
    location_detail_view,
    recommendations_page,
)

urlpatterns = [
    path("", landing_page, name="landing"),
    path("recommendations", recommendations_page, name="recommendations"),
    path("api/recommendations", get_recommendations, name="recommendations_api"),
    path("destinations", destinations_page, name="destinations"),
    path("destinations/<str:location>/", location_detail_view, name="location_detail"),
]
