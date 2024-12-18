from aiogram.types.input_file import FSInputFile
from .models import (
    Article,
    Match,
    Connection,
    Author,
    Category,
    ProgrammingLanguage,
    Book,
    Video,
)
from aiogram import Bot
from django.contrib import messages
from django.conf import settings
import asyncio

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
    actions = ["send_to_telegram_channel"]

    async def send_to_telegram(self, bot, channel_id, article):
        caption = f"<b>{article.title}</b>\n\n{article.body[:150]}..."
        caption += """<a href="https://shaxzodbek.com">Ko'proq o'qish</a>  """
        if article.picture:
            with open(article.picture.path, "rb") as photo:
                await bot.send_photo(
                    chat_id=channel_id,
                    photo=FSInputFile(path=article.picture.url),
                    caption=caption,
                    parse_mode="HTML",
                )
        else:
            await bot.send_message(chat_id=channel_id, text=caption, parse_mode="HTML")

    def send_to_telegram_channel(self, request, queryset):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        channel_id = settings.TELEGRAM_CHANNEL_ID

        for article in queryset:
            if not article.telegram:
                try:
                    asyncio.run(self.send_to_telegram(bot, channel_id, article))

                    article.telegram = True
                    article.save()
                    self.message_user(
                        request,
                        f"Successfully sent '{article.title}' to Telegram channel",
                        messages.SUCCESS,
                    )
                except Exception as e:
                    self.message_user(
                        request,
                        f"Failed to send '{article.title}' to Telegram channel: {str(e)}",
                        messages.ERROR,
                    )
            else:
                self.message_user(
                    request,
                    f"'{article.title}' has already been sent to Telegram",
                    messages.WARNING,
                )

        asyncio.run(bot.session.close())

    send_to_telegram_channel.short_description = (
        "Send selected articles to Telegram channel"
    )


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


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")
    ordering = ("first_name",)
    list_per_page = 25


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "programming_language", "picture_tag")
    list_filter = ("programming_language", "categories")
    search_fields = ("title", "purpose", "authors__first_name", "authors__last_name")
    ordering = ("title",)
    filter_horizontal = ("authors", "categories")
    readonly_fields = ("picture_preview",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "purpose",
                    "programming_language",
                    "authors",
                    "categories",
                )
            },
        ),
        (
            "Files",
            {
                "fields": ("book",),
            },
        ),
        (
            "Image",
            {
                "fields": ("picture", "picture_preview"),
            },
        ),
    )
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


@admin.register(AboutShe)
class CsrfExemptAdmin(AboutMeAdmin):
    pass
