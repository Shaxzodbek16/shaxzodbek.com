from django.contrib import admin
from django.utils.html import format_html
from .models import Math

@admin.register(Math)
class MathAdmin(admin.ModelAdmin):
    list_display = (
        'question_short', 'image_tag', 'answer', 'option1', 'option2', 'option3',
        'taken_book', 'theme', 'created_at', 'updated_at'
    )
    list_filter = ('created_at', 'updated_at', 'taken_book', 'theme')
    search_fields = (
        'question', 'answer', 'option1', 'option2', 'option3',
        'slug', 'taken_book', 'theme'
    )
    readonly_fields = ('slug', 'created_at', 'updated_at', 'image_preview')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'slug')
        }),
        ('Options', {
            'fields': ('option1', 'option2', 'option3'),
        }),
        ('Additional Info', {
            'fields': ('taken_book', 'theme'),
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    date_hierarchy = 'created_at'
    list_per_page = 25

    def question_short(self, obj):
        return obj.question[:50] + ('...' if len(obj.question) > 50 else '')
    question_short.short_description = 'Question'

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;"/>',
                obj.image.url
            )
        else:
            return 'No Image'
    image_tag.short_description = 'Image'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="300" height="300" style="object-fit: contain;"/>',
                obj.image.url
            )
        else:
            return 'No Image'
    image_preview.short_description = 'Image Preview'
