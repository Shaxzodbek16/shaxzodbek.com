from django.urls import path
from .views import cv, cvs, about_me

urlpatterns = [
    path('', cvs, name='cvs'),
    path('aboutme/', about_me, name='about_me'),
    path('<slug:slug>/', cv, name='cv'),

]
