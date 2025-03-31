from django.urls import path

from . import api
from .views import community_reviews

urlpatterns = [
    path("", community_reviews, name="community_reviews"),
    # API
    path("api/reviews", api.community_reviews, name="community_reviews"),
    path("api/places", api.places_list, name="places_list"),
    path("api/review/add", api.add_review, name="add_review"),
    path("api/review/<int:id>/reply", api.add_reply, name="add_reply"),
    path("api/review/<int:id>/like", api.like_review, name="like_review"),
]
