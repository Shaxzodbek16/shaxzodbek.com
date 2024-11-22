from django.urls import path

from telegrambot.views import TelegramUserListCreateAPIView, CommandsListCreateAPIView, FeedbackListCreateAPIView, \
    TelegramUserRetrieveUpdateAPIView

urlpatterns = [
    path('create_user/', TelegramUserListCreateAPIView.as_view(), name='telegram_user_list_create'),
    path('create_user/<str:user_id>/', TelegramUserRetrieveUpdateAPIView.as_view(), name='user-update'),
    path('user_commands/', CommandsListCreateAPIView.as_view(), name='telegram_command_list_create'),
    path('feedback/', FeedbackListCreateAPIView.as_view(), name='telegram_feedback_list_create'),
]
