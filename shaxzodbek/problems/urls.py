# urls.py

from django.urls import path
from .views import a

urlpatterns = [
    path('problems/',a, name='problem_list'),
    path('problems/<slug:slug>/', a, name='problem_detail'),
    path('problems/<slug:slug>/solve/', a, name='solve_problem'),

    path('admin/problems/add/', a, name='problem_add'),
    path('admin/problems/<slug:slug>/edit/', a, name='problem_edit'),
    path('admin/problems/<slug:slug>/delete/', a, name='problem_delete'),

    path('admin/images/add/', a, name='img_add'),
    path('admin/images/<int:pk>/edit/', a, name='img_edit'),
    path('admin/images/<int:pk>/delete/', a, name='img_delete'),

    path('admin/examples/add/', a, name='example_add'),
    path('admin/examples/<int:pk>/edit/', a, name='example_edit'),
    path('admin/examples/<int:pk>/delete/', a, name='example_delete'),

    path('admin/topics/add/', a, name='topic_add'),
    path('admin/topics/<int:pk>/edit/', a, name='topic_edit'),
    path('admin/topics/<int:pk>/delete/', a, name='topic_delete'),

    path('admin/hints/add/', a, name='hint_add'),
    path('admin/hints/<int:pk>/edit/', a, name='hint_edit'),
    path('admin/hints/<int:pk>/delete/', a, name='hint_delete'),
]
