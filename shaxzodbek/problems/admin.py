from django.contrib import admin
from .models import (
    Img, Example, Topic, Hint, Files, Theme, Problem,
    TestCase, Submission, TestResult, UserProblemStatus
)

@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('input', 'output', 'description')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('hint',)

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('title',)

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created', 'updated')
    list_filter = ('difficulty',)
    search_fields = ('title',)
    filter_horizontal = ('images', 'examples', 'topics', 'hints', 'solved_users', 'files', 'theme')
    readonly_fields = ('slug', 'created', 'updated')

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('problem', 'order', 'is_sample')
    list_filter = ('is_sample',)
    search_fields = ('problem__title',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'status', 'submitted_at')
    list_filter = ('status', 'language')
    search_fields = ('user__username', 'problem__title')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('submission', 'test_case', 'passed')
    list_filter = ('passed',)
    search_fields = ('submission__user__username',)

@admin.register(UserProblemStatus)
class UserProblemStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'is_solved', 'attempts_count')
    list_filter = ('is_solved',)
    search_fields = ('user__username', 'problem__title')