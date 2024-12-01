from django.shortcuts import render
import datetime

from .models import Article, Connection, Category, ProgrammingLanguage, Book, Video
from .helpers import group_articles, make_unique
from django.db.models import Q


def calculate_age(birth_date):
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def root(request):
    return render(request, 'home.html', context={"age": calculate_age(datetime.date(1990, 1, 1))})


def articles(request):
    grouped_articles = group_articles(Article.objects.all())
    return render(request, 'blog/articles.html', context={"grouped_articles": grouped_articles})


def article(request, slug):
    try:
        result = Article.objects.get(slug=slug)
        return render(request, 'blog/article.html', context={"article": result})
    except Article.DoesNotExist:
        return render(request, 'blog/article.html', context={"article": []})


def video(request):
    return render(request, 'blog/video.html', context={"videos": Video.objects.all()})


def books(request):
    categories = Category.objects.values_list('name', flat=True)
    languages = ProgrammingLanguage.objects.values_list('name', flat=True)

    if request.method == 'POST':
        query = request.POST.get('search', '')
        if query:
            result = Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(programming_language__name__icontains=query)
            ).distinct()
            return render(request, 'blog/books.html', {
                "books": result,
                "pg_lang": languages,
                "categories": categories,
                "current_value": query
            })

    return render(request, 'blog/books.html', {
        "books": Book.objects.all(),
        "pg_lang": languages,
        "categories": categories
    })


def connections(request):
    query = request.POST.get('search', '') if request.method == 'POST' else ''
    filter_conditions = Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(job_title__icontains=query) | Q(met_address__icontains=query) | Q(home_address__icontains=query) | Q(who_for_me__who_is_it__icontains=query)

    if request.user.is_superuser:
        result = Connection.objects.filter(filter_conditions) if query else Connection.objects.all()
    else:
        result = Connection.objects.filter(listed=True).filter(filter_conditions) if query else Connection.objects.filter(listed=True)

    return render(request, 'blog/connections.html', context={"people": list(set(result)), "current_value": query})



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
            result = (AboutMe.objects.filter(title__icontains=query))
            return render(request, 'cv/about_me.html',
                          context={"information": result, "current_value": query})
    return render(request, 'cv/about_me.html', {"information": AboutMe.objects.all()})
