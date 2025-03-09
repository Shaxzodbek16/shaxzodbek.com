from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Article,
    ProgrammingLanguage,
    Education,
    Certification,
    Project,
    Type,
    CV,
)


def image_preview(obj):
    if obj.image:
        return format_html(
            '<img src="{}" width="50" height="50" style="border-radius:5px;" />',
            obj.image.url,
        )
    return "(No Image)"


image_preview.allow_tags = True
image_preview.short_description = "Preview"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", image_preview, "created", "visible")
    search_fields = ("title", "content1", "content2")
    list_filter = ("created",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", image_preview, "started_from")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("name", image_preview, "started_from", "ended_at", "field")
    search_fields = ("name", "description")
    list_filter = ("started_from", "ended_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", image_preview, "took_at")
    search_fields = ("name", "description")
    list_filter = ("took_at",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", image_preview, "started_from", "ended_at")
    search_fields = ("name", "description")
    list_filter = ("started_from", "ended_at")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("programming_languages",)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(CV)
