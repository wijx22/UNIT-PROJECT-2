from django.urls import path

from . import api
from .views import login_view, logout_view, signup_view, user_profile

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # API
    path(
        "update-profile-picture/",
        api.update_profile_picture,
        name="update_profile_picture",
    ),
    path("update-user-info/", api.update_user_info, name="update_user_info"),
    path("delete-review/", api.delete_review, name="delete_review"),
]
