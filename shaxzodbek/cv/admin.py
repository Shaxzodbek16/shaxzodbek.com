from django.contrib import admin
from .models import CV, Technology, CVImages, AboutMe

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('title', 'created_at')
    search_fields = ('title', 'description', 'technologies__name')
    filter_horizontal = ('picture', 'technologies')
    ordering = ('title','created_at')

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(CVImages)
class CVImagesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'extra_data', 'location')
    list_filter = ('title', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('title','created_at')



