from django.urls import path

from .views import root, article, articles, video, books, connections
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path("", root, name="root"),
    path("articles/", articles, name="articles"),
    path("articles/<str:slug>/", article, name="article"),
    path("video/", video, name="video"),
    path("books/", books, name="books"),
    path("connections/", connections, name="connections"),
]
