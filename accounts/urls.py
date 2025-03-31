from django.urls import path

from .views import login_view, logout_view, signup_view, user_profile

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
