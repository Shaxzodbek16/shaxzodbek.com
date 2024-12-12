from django.urls import path
from .views import a

urlpatterns = [
    path("problems/", a, name="problem_list"),
    path("problems/<slug:slug>/", a, name="problem_detail"),
]
