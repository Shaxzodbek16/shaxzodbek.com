from django.contrib import admin
from .models import Img, Example, Topic, Hint, Files, Theme, Problem


@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("input", "output", "description")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("hint",)


@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    search_fields = ("title",)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "created", "updated")
    list_filter = ("difficulty",)
    search_fields = ("title",)
    filter_horizontal = (
        "images",
        "examples",
        "topics",
        "hints",
        "solved_users",
        "files",
        "theme",
    )
    readonly_fields = ("slug", "created", "updated")
