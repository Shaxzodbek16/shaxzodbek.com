from rest_framework import serializers
from .models import Math


class MathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Math
        exclude = ('id',)
        read_only_fields = ('slug', 'created_at', 'updated_at')


class MathListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Math
        exclude = ('id',)
        read_only_fields = ('slug', 'created_at', 'updated_at')


class CheckAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=100)
