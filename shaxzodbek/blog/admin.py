from .models import Article,Match,Connection, Video
from django.contrib import admin
from django.utils.html import format_html
from .models import Technology, CVImages, CV, AboutMe, AboutShe


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "description_short")
    search_fields = ("name", "description")
    ordering = ("name",)
    list_per_page = 25

    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + ("..." if len(obj.description) > 50 else "")
        else:
            return "No Description"

    description_short.short_description = "Description"


@admin.register(CVImages)
class CVImagesAdmin(admin.ModelAdmin):
    list_display = ("name", "image_tag")
    search_fields = ("name",)
    readonly_fields = ("image_preview",)
    ordering = ("name",)
    list_per_page = 25
    fieldsets = (
        (None, {"fields": ("name",)}),
        (
            "Image",
            {
                "fields": ("image", "image_preview"),
            },
        ),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;"/>',
                obj.image.url,
            )
        else:
            return "No Image"

    image_tag.short_description = "Image"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="300" height="300" style="object-fit: contain;"/>',
                obj.image.url,
            )
        else:
            return "No Image"

    image_preview.short_description = "Image Preview"


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_working")
    list_filter = ("created_at", "is_working")
    search_fields = ("title", "description", "project_name", "technologies__name")
    ordering = ("-created_at",)
    filter_horizontal = ("picture", "technologies")
    readonly_fields = ("slug",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "project_name",
                    "path",
                    "is_working",
                )
            },
        ),
        (
            "Files",
            {
                "fields": ("file",),
            },
        ),
        (
            "Images",
            {
                "fields": ("picture",),
            },
        ),
        (
            "Technologies",
            {
                "fields": ("technologies",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
            },
        ),
    )
    date_hierarchy = "created_at"
    list_per_page = 25


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "image_tag")
    search_fields = ("title", "description", "extra_data", "location")
    ordering = ("-created_at",)
    readonly_fields = ("image_preview",)
    fieldsets = (
        (None, {"fields": ("title", "description", "extra_data", "location")}),
        (
            "Image",
            {
                "fields": ("image", "image_preview"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
            },
        ),
    )
    date_hierarchy = "created_at"
    list_per_page = 25

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;"/>',
                obj.image.url,
            )
        else:
            return "No Image"

    image_tag.short_description = "Image"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="300" height="300" style="object-fit: contain;"/>',
                obj.image.url,
            )
        else:
            return "No Image"

    image_preview.short_description = "Image Preview"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "picture_tag", "created", "updated", "telegram")
    list_filter = ("created", "updated", "telegram")
    search_fields = ("title", "body", "slug")
    readonly_fields = ("slug", "updated", "picture_preview")
    ordering = ("-created",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "body", "telegram")}),
        (
            "Image",
            {
                "fields": ("picture", "picture_preview"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created", "updated"),
            },
        ),
    )
    date_hierarchy = "created"
    list_per_page = 25

    def picture_tag(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;"/>',
                obj.picture.url,
            )
        else:
            return "No Image"

    picture_tag.short_description = "Picture"

    def picture_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="300" height="300" style="object-fit: contain;"/>',
                obj.picture.url,
            )
        else:
            return "No Image"

    picture_preview.short_description = "Picture Preview"


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("who_is_it", "created", "updated")
    list_filter = ("created", "updated")
    search_fields = ("who_is_it",)
    readonly_fields = ("created", "updated")
    ordering = ("-created",)
    date_hierarchy = "created"
    list_per_page = 25


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "picture_tag", "birth_date", "job_title", "listed")
    list_filter = ("listed", "birth_date", "met_at")
    search_fields = ("first_name", "last_name", "job_title", "who_for_me__who_is_it")
    readonly_fields = ("picture_preview",)
    ordering = ("-birth_date",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "job_title",
                    "birth_date",
                    "listed",
                )
            },
        ),
        (
            "Contact Info",
            {
                "fields": ("met_address", "home_address", "met_at", "who_for_me"),
            },
        ),
        (
            "Image",
            {
                "fields": ("picture", "picture_preview"),
            },
        ),
    )
    date_hierarchy = "birth_date"
    list_per_page = 25
    filter_horizontal = ("who_for_me",)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Full Name"

    def picture_tag(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;"/>',
                obj.picture.url,
            )
        else:
            return "No Image"

    picture_tag.short_description = "Picture"

    def picture_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="300" height="300" style="object-fit: contain;"/>',
                obj.picture.url,
            )
        else:
            return "No Image"

    picture_preview.short_description = "Picture Preview"



@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "thumbnail_tag", "description")
    list_filter = ("created_at",)
    search_fields = ("title", "url")
    ordering = ("-created_at",)
    readonly_fields = ("thumbnail_preview",)
    fieldsets = (
        (None, {"fields": ("title", "url", "created_at", "description")}),
        (
            "Image",
            {
                "fields": ("thumbnail", "thumbnail_preview"),
            },
        ),
    )
    date_hierarchy = "created_at"
    list_per_page = 25

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;"/>',
                obj.thumbnail.url,
            )
        else:
            return "No Image"

    thumbnail_tag.short_description = "Thumbnail"

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="300" height="300" style="object-fit: contain;"/>',
                obj.thumbnail.url,
            )
        else:
            return "No Image"

    thumbnail_preview.short_description = "Thumbnail Preview"


admin.site.register(AboutShe)
