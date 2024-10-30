from django.db import models
from slugify import slugify


class Theme(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)


class Example(models.Model):
    input_data = models.TextField()
    output_data = models.TextField()

    def __str__(self):
        return self.input_data

    class Meta:
        verbose_name = 'Example'
        verbose_name_plural = 'Examples'
        db_table = 'examples'
        ordering = ['input_data']


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'categories'
        ordering = ['name']


class Algorithm(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Algorithm'
        verbose_name_plural = 'Algorithms'
        db_table = 'algorithm'
        ordering = ['name']


class Problem(models.Model):
    difficulties = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    examples = models.ManyToManyField(Example)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    theme = models.ManyToManyField(Theme, related_name='themes')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=difficulties, default=difficulties[0][0])
    solution = models.TextField()
    initial_code = models.TextField(default="def solution(input):\n    # Write your code here\n    pass")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Problems'
        verbose_name = 'Problem'
        ordering = ['title']
        db_table = 'problems'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    output_data = models.TextField()
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"Test case for {self.problem.title}"

    class Meta:
        ordering = ['id']
