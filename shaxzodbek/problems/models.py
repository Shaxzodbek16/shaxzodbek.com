from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Img(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="problems/%Y/%m/%d/")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Img"
        ordering = ("title",)
        verbose_name = "Image"
        verbose_name_plural = "Images"


class Example(models.Model):
    input = models.TextField()
    output = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"Example: {self.description[:50]}"

    class Meta:
        db_table = "Example"
        ordering = ("-id",)
        verbose_name = "Example"
        verbose_name_plural = "Examples"


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Topic"
        ordering = ("title",)
        verbose_name = "Topic"
        verbose_name_plural = "Topics"


class Hint(models.Model):
    hint = models.TextField()

    def __str__(self):
        return f"Hint: {self.hint[:50]}"

    class Meta:
        db_table = "Hint"
        ordering = ("-id",)
        verbose_name = "Hint"
        verbose_name_plural = "Hints"


class Files(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="problems/files/%Y/%m/%d/")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Files"
        ordering = ("title",)
        verbose_name = "Files"
        verbose_name_plural = "Files"


class Theme(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Theme"
        ordering = ("title",)
        verbose_name = "Theme"
        verbose_name_plural = "Themes"


class Problem(models.Model):
    DIFFICULTY_CHOICES = (
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    notes = models.TextField(blank=True)
    constraints = models.TextField(blank=True)
    solution = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    images = models.ManyToManyField(Img, blank=True, related_name="problems")
    examples = models.ManyToManyField(Example, blank=True, related_name="problems")
    topics = models.ManyToManyField(Topic, blank=True, related_name="problems")
    hints = models.ManyToManyField(Hint, blank=True, related_name="problems")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    solved_users = models.ManyToManyField(
        User, blank=True, related_name="solved_problems"
    )
    files = models.ManyToManyField(Files, blank=True, related_name="problems_files")
    theme = models.ManyToManyField(Theme, blank=True, related_name="theme_problems")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Problem"
        ordering = ("-created",)
        verbose_name = "Problem"
        verbose_name_plural = "Problems"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            original_slug = slugify(self.title)
            slug = original_slug
            num = 1
            while Problem.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{original_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
