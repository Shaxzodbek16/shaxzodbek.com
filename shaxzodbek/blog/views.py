from django.http import HttpResponse
from django.shortcuts import render, redirect
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
    result = Article.objects.get(slug=slug)
    return render(request, 'blog/article.html', context={"article": result})


def video(request):
    return render(request, 'blog/video.html', context={"videos": Video.objects.all()})


def books(request):
    names: set = make_unique(ProgrammingLanguage.objects.all())
    names |= make_unique(Category.objects.all())
    categories = [category.name for category in Category.objects.all()]
    languages = [language.name for language in ProgrammingLanguage.objects.all()]
    if request.method == 'POST':
        query = request.POST['search']
        if query:
            result = (Book.objects.filter(title__icontains=query) &
                      Book.objects.filter(author__last_name__icontains=query) &
                      Book.objects.filter(author__first_name__icontains=query) &
                      Book.objects.filter(programming_language__name__icontains=query))
            return render(request, 'blog/books.html',
                          context={"books": result, "pg_lang": languages, "categories": categories,
                                   "current_value": query})
    return render(request, 'blog/books.html',
                  context={"books": Book.objects.all(), "pg_lang": languages, "categories": categories})


def connections(request):
    if request.method == 'POST':
        query = request.POST['search']
        if query:
            if request.user.is_superuser:
                result = Connection.objects.filter(
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(job_title__icontains=query) |
                    Q(met_address__icontains=query) |
                    Q(home_address__icontains=query) |
                    Q(who_for_me__who_is_it__icontains=query)
                )
            else:
                result = Connection.objects.filter(listed=True).filter(
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(job_title__icontains=query) |
                    Q(met_address__icontains=query) |
                    Q(home_address__icontains=query) |
                    Q(who_for_me__who_is_it__icontains=query)
                )
            return render(request, 'blog/connections.html', context={"people": list(set(result)), "current_value": query})

    if request.user.is_superuser:
        people = Connection.objects.all()
    else:
        people = Connection.objects.filter(listed=True)
    return render(request, 'blog/connections.html', context={"people": people})


def admin(request):
    return HttpResponse(
        "Hello, I thought you did not learn IT to destroy, now I know why you learnt, thank to your teacher.")


def upload(request):
    return redirect('admin')
