from django.urls import path

from .views import community_reviews

urlpatterns = [
    path("", community_reviews, name="community_reviews"),
]
