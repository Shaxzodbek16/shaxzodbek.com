from django.urls import path
from .views import (
    home,
    articles,
    article_detail,
    certifications,
    certification_detail,
    projects,
    project_detail,
    aboutme,
)

app_name = "blog"

urlpatterns = [
    path("", home, name="home"),
    path("aboutme/", aboutme, name="aboutme"),
    path("articles/", articles, name="articles"),
    path("articles/<slug:slug>/", article_detail, name="article_detail"),
    path("certifications/", certifications, name="certifications"),
    path(
        "certifications/<slug:slug>/",
        certification_detail,
        name="certification_detail",
    ),
    path("projects/", projects, name="projects"),
    path("projects/<slug:slug>/", project_detail, name="project_detail"),
]
