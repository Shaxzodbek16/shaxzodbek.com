from django.contrib import admin
from django.utils.html import format_html
from .models import Img, Example, Topic, Hint, Problem

@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')
    search_fields = ('title',)
    readonly_fields = ('image_preview',)
    ordering = ('title',)
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;" alt="{}"/>',
                obj.image.url,
                obj.title
            )
        else:
            return 'No Image'
    image_tag.short_description = 'Image'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="300" height="300" style="object-fit: contain;" alt="{}"/>',
                obj.image.url,
                obj.title
            )
        else:
            return 'No Image'
    image_preview.short_description = 'Image Preview'

@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('input_short', 'output_short', 'description_short')
    search_fields = ('input', 'output', 'description')
    ordering = ('-id',)
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': ('input', 'output', 'description')
        }),
    )

    def input_short(self, obj):
        return obj.input[:50] + ('...' if len(obj.input) > 50 else '')
    input_short.short_description = 'Input'

    def output_short(self, obj):
        return obj.output[:50] + ('...' if len(obj.output) > 50 else '')
    output_short.short_description = 'Output'

    def description_short(self, obj):
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
    description_short.short_description = 'Description'

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_short')
    search_fields = ('title', 'description')
    ordering = ('-id',)
    list_per_page = 25

    def description_short(self, obj):
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
    description_short.short_description = 'Description'

@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('hint_short',)
    search_fields = ('hint',)
    ordering = ('-id',)
    list_per_page = 25

    def hint_short(self, obj):
        return obj.hint[:50] + ('...' if len(obj.hint) > 50 else '')
    hint_short.short_description = 'Hint'

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title_short', 'difficulty', 'created', 'updated')
    list_filter = ('difficulty', 'created', 'updated')
    search_fields = ('title', 'description', 'notes', 'constraints', 'solution')
    ordering = ('-created',)
    filter_horizontal = ('images', 'examples', 'topics', 'hints', 'solved_users')
    readonly_fields = ('slug', 'created', 'updated')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'notes', 'constraints', 'solution', 'difficulty')
        }),
        ('Associations', {
            'fields': ('images', 'examples', 'topics', 'hints', 'solved_users')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
        }),
    )
    date_hierarchy = 'created'
    list_per_page = 25

    def title_short(self, obj):
        return obj.title[:50] + ('...' if len(obj.title) > 50 else '')
    title_short.short_description = 'Title'
