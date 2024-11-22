from rest_framework import serializers
from .models import Questions


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        exclude = ('id',)
        read_only_fields = ('slug', 'created_at', 'updated_at')


class QuestionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        exclude = ('id',)
        read_only_fields = ('slug', 'created_at', 'updated_at')


class CheckAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=100)
