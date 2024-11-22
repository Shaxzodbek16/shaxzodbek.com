from .models import TelegramUser, Commands, Feedback
from rest_framework import serializers


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('user_id', 'first_name', 'last_name', 'username', 'phone_number')


class CommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commands
        fields = ('user', 'command', 'message', 'response')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('user', 'message', 'file')
