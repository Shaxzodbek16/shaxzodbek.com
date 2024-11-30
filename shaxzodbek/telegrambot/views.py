from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import SearchFilter

from .models import TelegramUser
from .serializers import TelegramUserSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class TelegramUserListCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['user_id']


class TelegramUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    lookup_field = 'user_id'  # Use 'user_id' as the slug fo
