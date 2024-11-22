from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionsViewSet, docs, statistics

router = DefaultRouter()
router.register(r'math', QuestionsViewSet, basename='math')

urlpatterns = [
    path('docs/', docs, name='docs'),
    path('docs/<str:api_name>/', docs, name='docs_with_api'),
    path('statistics/', statistics, name='statistics'),
    path('', include(router.urls)),
]
