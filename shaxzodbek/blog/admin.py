from django.contrib import admin
from .models import Article, Match, Connection, Author, Category, ProgrammingLanguage, Book, Video


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('title', 'body')
    date_hierarchy = 'created'
    ordering = ('-created',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('who_is_it', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('who_is_it',)
    date_hierarchy = 'created'
    ordering = ('-created',)


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job_title', 'birth_date', "home_address")
    list_filter = ('birth_date', 'job_title')
    search_fields = ('first_name', 'last_name', 'job_title', 'met_at')
    date_hierarchy = 'birth_date'
    filter_horizontal = ('who_for_me',)
    ordering = ('-birth_date',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('-first_name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-name',)


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'purpose', 'programming_language')
    list_filter = ('programming_language', 'category')
    search_fields = ('title', 'purpose', 'author__first_name', 'author__last_name')
    filter_horizontal = ('author', 'category')
    ordering = ('-title',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created')
    list_filter = ('title', 'created')
    search_fields = ('title', )
    ordering = ('-created',)
