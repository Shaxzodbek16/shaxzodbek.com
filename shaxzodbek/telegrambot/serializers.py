from .models import TelegramUser, UserCommands
from rest_framework import serializers


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('user_id', 'first_name', 'last_name', 'username', 'phone_number')


class UserCommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommands
        fields = ('user_id', 'command', 'created_at')
