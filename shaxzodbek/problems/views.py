from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Problem


def problems(request):
    return render(
        request, "problems/problems.html", {"problems": Problem.objects.all()}
    )


@login_required
def problem(request, slug):
    problem_ = Problem.objects.get(slug=slug)
    if problem_:
        return render(
            request, "problems/problem.html", {"problem": problem_}, status=200
        )
    return render(request, "404.html", status=404)
