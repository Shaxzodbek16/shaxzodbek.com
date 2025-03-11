from django.urls import path
from .views import (
    home,
    post_detail,
    post,
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
    path("post/", post, name="post"),
    path("articles/<slug:slug>/", post_detail, name="article_detail"),
    path("certifications/", certifications, name="certifications"),
    path(
        "certifications/<slug:slug>/",
        certification_detail,
        name="certification_detail",
    ),
    path("projects/", projects, name="projects"),
    path("projects/<slug:slug>/", project_detail, name="project_detail"),
]
