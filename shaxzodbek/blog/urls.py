from django.urls import path

from .views import (
    root,
    article,
    articles,
    videos,
    books,
    connections,
    cv,
    cvs,
    about_me,
    csrf_exempt_,
)

from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path("", root, name="root"),
    path("articles/", articles, name="articles"),
    path("articles/<str:slug>/", article, name="article"),
    path("videos/", videos, name="videos"),
    path("books/", books, name="books"),
    path("connections/", connections, name="connections"),
    path("cvs/", cvs, name="cvs"),
    path("cvs/<slug:slug>/", cv, name="cv"),
    path("aboutme/", about_me, name="about_me"),
    path(
        "secret/",
        staff_member_required(csrf_exempt(csrf_exempt_)),
        name="_csrf_exempt_",
    ),
]
