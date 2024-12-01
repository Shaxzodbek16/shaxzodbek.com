from django.urls import path

from .views import root, article, articles, video, books, connections, cv, cvs, about_me
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path("", root, name="root"),
    path("articles/", articles, name="articles"),
    path("articles/<str:slug>/", article, name="article"),
    path("video/", video, name="video"),
    path("books/", books, name="books"),
    path("connections/", connections, name="connections"),

    path('', cvs, name='cvs'),
    path('aboutme/', about_me, name='about_me'),
    path('<slug:slug>/', cv, name='cv'),



]
