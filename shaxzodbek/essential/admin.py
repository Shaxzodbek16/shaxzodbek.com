from django.contrib import admin
from .models import Example, Category, Algorithm, Problem, TestCase

@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('input_data', 'output_data')
    search_fields = ('input_data', 'output_data')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'theme', 'algorithm', 'difficulty', 'initial_code')
    list_filter = ('difficulty', 'theme', 'algorithm')
    search_fields = ('title', 'description')
    filter_horizontal = ('examples',)
    # Remove prepopulated_fields since slug is auto-generated
    readonly_fields = ('slug',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'difficulty')
        }),
        ('Relations', {
            'fields': ('theme', 'algorithm', 'examples')
        }),
        ('Additional Information', {
            'fields': ('image', 'note', 'solution', 'slug'),
        }),
    )
@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('problem', 'input_data', 'output_data', 'is_hidden')
    list_filter = ('problem', 'is_hidden')
    search_fields = ('problem__title', 'input_data', 'output_data')