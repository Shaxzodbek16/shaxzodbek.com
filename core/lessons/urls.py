from django.urls import  path
from .views import get_lessons

app_name = 'lessons'

urlpatterns = [
    path('lessons/',get_lessons , name='lessons'),
]

