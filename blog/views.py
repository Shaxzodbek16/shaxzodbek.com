from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import (
    Post,
    ProgrammingLanguage,
    Education,
    Certification,
    Project,
    CV,
    AboutMe,
)
from django.views.decorators.cache import cache_page
from typing import Any


@cache_page(60)
def home(request):
    context = {
        "programming_languages": ProgrammingLanguage.objects.all().order_by(
            "-knowing_percentage"
        ),
        "educations": Education.objects.all(),
        "posts": Post.objects.filter(visible=True),
        "projects": Project.objects.all()[:4],
        "cv": CV.objects.all().first(),
    }
    return render(request, "home.html", context)


@cache_page(60)
def aboutme(request):
    items = AboutMe.objects.all()  # thanks to Meta.ordering newest first
    return render(request, "aboutme.html", {"items": items})


def paginated_view(request, model: Any, template, order_by="-id", per_page=6):
    object_list = model.objects.all().order_by(order_by)
    paginator = Paginator(object_list, per_page)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, template, {"page_obj": page_obj})


@cache_page(60)
def post(request):
    return paginated_view(request, Post, "blog/post.html", order_by="-created")


@cache_page(60)
def certifications(request):
    return paginated_view(request, Certification, "blog/certifications.html")


@cache_page(60)
def projects(request):
    return paginated_view(
        request, Project, "blog/projects.html", order_by="-started_from"
    )


def detail_view(request, model, slug, template):
    obj = get_object_or_404(model, slug=slug)
    context = {
        model.__name__.lower(): obj,
        f"next_{model.__name__.lower()}": getattr(obj, "next", None),
        f"previous_{model.__name__.lower()}": getattr(obj, "previous", None),
    }
    return render(request, template, context)


def post_detail(request, slug):
    return detail_view(request, Post, slug, "blog/post_detail.html")


def certification_detail(request, slug):
    return detail_view(request, Certification, slug, "blog/certification_detail.html")


def project_detail(request, slug):
    return detail_view(request, Project, slug, "blog/project_detail.html")
