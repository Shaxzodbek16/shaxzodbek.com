from django.http.response import HttpResponse
from django.shortcuts import render

def get_lessons(request):
    return HttpResponse('Hello')