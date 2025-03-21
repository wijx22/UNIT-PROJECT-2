from django.urls import path

from .views import landing_page,recommendations_page

urlpatterns = [
    path("", landing_page, name="landing"),
    path("recommendations", recommendations_page, name="recommendations"),
]

