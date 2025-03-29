from django.urls import path

from .views import (
    booking_api,
    booking_page,
    destinations_page,
    get_recommendations,
    landing_page,
    location_detail_view,
    place_details,
    recommendations_page,
)

urlpatterns = [
    path("", landing_page, name="landing"),
    path("recommendations", recommendations_page, name="recommendations"),
    path("api/recommendations", get_recommendations, name="recommendations_api"),
    path("destinations", destinations_page, name="destinations"),
    path("destinations/<str:location>/", location_detail_view, name="location_detail"),
    path(
        "destinations/<str:location>/places/<int:place_id>/",
        place_details,
        name="place_details",
    ),
    path("booking/<int:service_id>/<int:place_id>/", booking_page, name="booking"),
    path("api/booking", booking_api, name="booking_api"),
]
