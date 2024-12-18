from django.urls import path
from .views import (
    signup_view,
    verify_email,
    login_view,
    logout_view,
    user_profile,
    password_reset_confirm,
    password_reset_request,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("verify-email/<slug:slug>/", verify_email, name="verify_email"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/<slug:slug>", user_profile, name="profile"),
    path("password-reset/", password_reset_request, name="password_reset_request"),
    path(
        "password-reset/<str:token>/",
        password_reset_confirm,
        name="password_reset_confirm",
    ),
]
