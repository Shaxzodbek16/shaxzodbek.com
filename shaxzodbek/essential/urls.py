from django.urls import path
from . import views

app_name = 'problems'

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('create/', views.problem_create, name='problem_create'),
    path('<slug:slug>/', views.problem_detail, name='problem_detail'),
    path('<slug:slug>/update/', views.problem_update, name='problem_update'),
    path('<slug:slug>/delete/', views.problem_delete, name='problem_delete'),
    path('problems/<int:problem_id>/execute/', views.execute_solution, name='execute_solution'),
]
