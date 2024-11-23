from .models import TelegramUser
from rest_framework import serializers


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('user_id', 'first_name', 'last_name', 'username', 'phone_number')

