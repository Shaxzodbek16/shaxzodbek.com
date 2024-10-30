from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Problem
from .forms import ProblemForm
from django.contrib import messages
from django.http import JsonResponse
from .utils import execute_code


def is_admin(user):
    return user.is_superuser


def problem_list(request):
    problem_list = Problem.objects.all().order_by('title')
    paginator = Paginator(problem_list, 10)

    page = request.GET.get('page')
    problems = paginator.get_page(page)

    return render(request, 'problems/problem_list.html', {
        'problems': problems,
        'is_admin': request.user.is_superuser
    })


@require_http_methods(["GET"])
def problem_detail(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'is_admin': request.user.is_superuser
    })


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def problem_create(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            problem = form.save()
            messages.success(request, 'Problem created successfully!')
            return redirect('problem_detail', slug=problem.slug)
    else:
        form = ProblemForm()

    return render(request, 'problems/problem_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def problem_update(request, slug):
    problem = get_object_or_404(Problem, slug=slug)

    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES, instance=problem)
        if form.is_valid():
            problem = form.save()
            messages.success(request, 'Problem updated successfully!')
            return redirect('problem_detail', slug=problem.slug)
    else:
        form = ProblemForm(instance=problem)

    return render(request, 'problems/problem_form.html', {
        'form': form,
        'problem': problem,
        'action': 'Update'
    })


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def problem_delete(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    problem.delete()
    messages.success(request, 'Problem deleted successfully!')
    return redirect('problem_list')


@login_required
def execute_solution(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    code = request.POST.get('code')

    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    # Get test cases
    test_cases = []
    for test_case in problem.test_cases.filter(is_hidden=False):
        test_cases.append({
            'input': test_case.input_data,
            'output': test_case.output_data
        })

    try:
        result = execute_code(code, test_cases)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

