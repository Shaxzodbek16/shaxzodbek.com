from django.urls import path

from telegrambot.views import (
    TelegramUserListCreateAPIView,
    TelegramUserRetrieveUpdateAPIView,
    UserCommandsListCreateAPIView,
)

urlpatterns = [
    path(
        "create_user/",
        TelegramUserListCreateAPIView.as_view(),
        name="telegram_user_list_create",
    ),
    path(
        "create_user/<str:user_id>/",
        TelegramUserRetrieveUpdateAPIView.as_view(),
        name="user-update",
    ),
    path(
        "create_command/",
        UserCommandsListCreateAPIView.as_view(),
        name="user_command_list_create",
    ),
]
