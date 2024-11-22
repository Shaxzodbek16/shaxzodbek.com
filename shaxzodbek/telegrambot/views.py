from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import TelegramUser, Commands, Feedback
from .serializers import TelegramUserSerializer, CommandsSerializer, FeedbackSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class TelegramUserListCreateAPIView(ListCreateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['user_id']


class TelegramUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    lookup_field = 'user_id'  # Use 'user_id' as the slug fo

class CommandsListCreateAPIView(ListCreateAPIView):
    queryset = Commands.objects.all()
    serializer_class = CommandsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = []
    search_fields = []

class FeedbackListCreateAPIView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = []
    search_fields = []
