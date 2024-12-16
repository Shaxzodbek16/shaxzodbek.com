from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import api_view
from .pagination import QuestionsPagination

from .models import Questions
from .serializers import (
    QuestionsSerializer,
    QuestionsListSerializer,
    CheckAnswerSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from authentication.models import User
from problems.models import Problem
from django.db.models import Count
from django.db.models.functions import TruncYear, TruncMonth


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    lookup_field = "slug"
    pagination_class = QuestionsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["theme", "taken_book"]  # Fields you can filter on
    search_fields = ["question", "theme", "taken_book"]  # Fields you can search

    def get_serializer_class(self):
        if self.action == "list":
            return QuestionsListSerializer
        return QuestionsSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"], url_path="check")
    def check_answer(self, request, slug=None):
        question_problem = self.get_object()
        serializer = CheckAnswerSerializer(data=request.data)

        if serializer.is_valid():
            user_answer = serializer.validated_data["answer"]
            is_correct = user_answer == question_problem.answer

            return Response(
                {
                    "correct": is_correct,
                    "message": (
                        "Correct answer!" if is_correct else "Wrong answer, try again."
                    ),
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@api_view(["GET"])
def statistics(request):
    user_stats = (
        User.objects.annotate(
            year=TruncYear("date_joined"), month=TruncMonth("date_joined")
        )
        .values("year", "month")
        .annotate(count=Count("id"))
        .order_by("year", "month")
    )

    user_counts = [
        {
            "year": stat["year"].year,
            "month": stat["month"].month,
            "user_count": stat["count"],
        }
        for stat in user_stats
    ]

    users = User.objects.all()
    problems = Problem.objects.all()
    solved_problems = sum(len(problem.solved_users.all()) for problem in problems)

    return Response(
        {
            "user_count": len(users),
            "problem_count": solved_problems,
            "problems": len(problems),
            "user_statistics": user_counts,
        }
    )


def docs(request, api_name=None):
    if not api_name:
        return render(request, template_name="api/questions.html")
    return render(request, template_name=f"api/questions.html")
