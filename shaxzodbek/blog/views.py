from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import datetime
from django.core.paginator import Paginator

from .models import (
    Article,
    Connection,
    Video,
    AboutShe,
    CV,
    AboutMe,
)
from .helpers import group_articles
from django.db.models import Q


def calculate_age(birth_date):
    today = datetime.date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age


def root(request):
    videos_4 = Video.objects.all()[:4]
    age = calculate_age(datetime.date(2005, 8, 16))

    return render(
        request,
        "blog/home.html",
        context={"age": age, "videos": videos_4},
    )


def articles(request):
    grouped_articles = group_articles(Article.objects.all())
    return render(
        request, "blog/articles.html", context={"grouped_articles": grouped_articles}
    )


def article(request, slug):
    try:
        result = Article.objects.get(slug=slug)
        return render(request, "blog/article.html", context={"article": result})
    except Article.DoesNotExist:
        return render(request, "blog/article.html", context={"article": []})


def videos(request):
    return render(request, "blog/videos.html", context={"videos": Video.objects.all()})



def connections(request):
    query = request.POST.get("search", "") if request.method == "POST" else ""
    filter_conditions = (
        Q(first_name__icontains=query)
        | Q(last_name__icontains=query)
        | Q(job_title__icontains=query)
        | Q(met_address__icontains=query)
        | Q(home_address__icontains=query)
        | Q(who_for_me__who_is_it__icontains=query)
    )

    if request.user.is_superuser:
        result = (
            Connection.objects.filter(filter_conditions)
            if query
            else Connection.objects.all()
        )
    else:
        result = (
            Connection.objects.filter(listed=True).filter(filter_conditions)
            if query
            else Connection.objects.filter(listed=True)
        )

    paginator = Paginator(result, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/connections.html",
        context={"page_obj": page_obj, "current_value": query},
    )


def cvs(request):
    if request.method == "POST":
        query = request.POST["search"]
        if query:
            result = (
                CV.objects.filter(title__icontains=query)
                & CV.objects.filter(technologies__icontains=query)
                & CV.objects.filter(path__icontains=query)
            )
            return render(
                request,
                "blog/cvs.html",
                context={"cvs": result, "current_value": query},
            )
    return render(request, "blog/cvs.html", {"cvs": CV.objects.all()})


@login_required
def cv(request, slug):
    return render(request, "blog/cv.html", {"cv": CV.objects.get(slug=slug)})


def about_me(request):
    if request.method == "POST":
        query = request.POST["search"]
        if query:
            result = AboutMe.objects.filter(title__icontains=query)
            return render(
                request,
                "blog/about_me.html",
                context={"information": result, "current_value": query},
            )
    return render(request, "blog/about_me.html", {"information": AboutMe.objects.all()})


def csrf_exempt_(request):
    return render(
        request, "blog/csrf_exempt.html", context={"about_she": AboutShe.objects.all()}
    )
