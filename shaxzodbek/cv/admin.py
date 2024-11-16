from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Technology,
    CVImages,
    CV,
    AboutMe,
)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 25

    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
        else:
            return 'No Description'
    description_short.short_description = 'Description'

@admin.register(CVImages)
class CVImagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    search_fields = ('name',)
    readonly_fields = ('image_preview',)
    ordering = ('name',)
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover;"/>', obj.image.url)
        else:
            return 'No Image'
    image_tag.short_description = 'Image'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="300" style="object-fit: contain;"/>', obj.image.url)
        else:
            return 'No Image'
    image_preview.short_description = 'Image Preview'

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_working')
    list_filter = ('created_at', 'is_working')
    search_fields = ('title', 'description', 'project_name', 'technologies__name')
    ordering = ('-created_at',)
    filter_horizontal = ('picture', 'technologies')
    readonly_fields = ('slug',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'project_name', 'path', 'is_working')
        }),
        ('Files', {
            'fields': ('file',),
        }),
        ('Images', {
            'fields': ('picture',),
        }),
        ('Technologies', {
            'fields': ('technologies',),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )
    date_hierarchy = 'created_at'
    list_per_page = 25

@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image_tag')
    search_fields = ('title', 'description', 'extra_data', 'location')
    ordering = ('-created_at',)
    readonly_fields = ('image_preview',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'extra_data', 'location')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )
    date_hierarchy = 'created_at'
    list_per_page = 25

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover;"/>', obj.image.url)
        else:
            return 'No Image'
    image_tag.short_description = 'Image'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="300" style="object-fit: contain;"/>', obj.image.url)
        else:
            return 'No Image'
    image_preview.short_description = 'Image Preview'
