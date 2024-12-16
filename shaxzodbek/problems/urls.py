from django.urls import path
from .views import problems, problem

urlpatterns = [
    path("problems/", problems, name="problems"),
    path("problems/<slug:slug>/", problem, name="problem"),
]
