from django.shortcuts import render
from .models import CV, AboutMe


def cvs(request):
    if request.method == 'POST':
        query = request.POST['search']
        if query:
            result = (CV.objects.filter(title__icontains=query) &
                      CV.objects.filter(technologies__icontains=query) &
                      CV.objects.filter(path__icontains=query))
            return render(request, 'cv/cvs.html',
                          context={"cvs": result, "current_value": query})
    return render(request, 'cv/cvs.html', {'cvs': CV.objects.all()})


def cv(request, slug): return render(request, 'cv/cv.html', {'cv': CV.objects.get(slug=slug)})


def about_me(request):
    if request.method == 'POST':
        query = request.POST['search']
        if query:
            result = (AboutMe.objects.filter(title__icontains=query) &
                      AboutMe.objects.filter(extra_data__icontains=query))
            return render(request, 'cv/about_me.html',
                          context={"information": result, "current_value": query})
    return render(request, 'cv/about_me.html', {"information": AboutMe.objects.all()})
