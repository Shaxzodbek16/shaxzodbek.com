import uuid

from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    picture = models.ImageField(
        upload_to="blog/articles/%Y/%m/%d", blank=True, null=True
    )
    body = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, default=str(uuid.uuid4()), blank=True, null=True
    )
    telegram = models.BooleanField(default=False)

    @property
    def prev(self):
        return Article.objects.filter(id__lt=self.id).order_by("-created").first()

    @property
    def next(self):
        return Article.objects.filter(id__gt=self.id).order_by("-created").first()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        db_table = "articles"


class Match(models.Model):
    who_is_it = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.who_is_it

    class Meta:
        ordering = ["-created"]
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        db_table = "matches"


class Connection(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="blog/connection/%Y/%m/%d")
    birth_date = models.DateField()
    job_title = models.CharField(max_length=255, blank=True, null=True)
    met_address = models.TextField()
    home_address = models.TextField(null=True, blank=True)
    met_at = models.DateTimeField()
    who_for_me = models.ManyToManyField(Match, related_name="who_me")
    listed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.job_title} {self.birth_date} {self.who_for_me}"

    class Meta:
        ordering = ["-birth_date"]
        verbose_name = "Connection"
        verbose_name_plural = "Connections"
        db_table = "connections"


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-first_name"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = "author"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "category"


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        verbose_name = "ProgrammingLanguage"
        verbose_name_plural = "ProgrammingLanguages"
        db_table = "programmingLanguage"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, related_name="books_author")
    purpose = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="blog/book/%Y/%m/%d")
    book = models.FileField(upload_to="blog/files/book/%Y/%m/%d")
    programming_language = models.ForeignKey(
        ProgrammingLanguage, on_delete=models.DO_NOTHING
    )
    category = models.ManyToManyField(Category, related_name="books_categories")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-title"]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = "book"


class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    created = models.DateTimeField()
    thumbnail = models.ImageField(upload_to="blog/video/%Y/%m/%d")

    def __str__(self):
        return f"{self.title} at {self.created}"

    class Meta:
        ordering = ["-created"]
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        db_table = "video"


from django.db import models
from slugify import slugify


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Technologies"
        verbose_name = "Technology"
        ordering = ["name"]
        db_table = "technologies"


class CVImages(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cv/cvImages/%Y/%m/%d/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "CV Images"
        verbose_name = "CV Image"
        ordering = ["name"]
        db_table = "cv_images"


class CV(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ManyToManyField(CVImages, related_name="cv_pictures")
    file = models.FileField(upload_to="cv/cvFiles/%Y/%m/%d/", blank=True, null=True)
    technologies = models.ManyToManyField(Technology, related_name="cv_pictures")
    path = models.URLField(null=True, blank=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField()
    is_working = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "CVs"
        verbose_name = "CV"
        ordering = ["-created_at"]
        db_table = "cvs"


class AboutMe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="cv/aboutMe/%Y/%m/%d/", null=True, blank=True)
    extra_data = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "About Me"
        verbose_name = "About Me"
        ordering = ["-created_at"]
        db_table = "about_me"


class AboutShe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="cv/aboutShe/%Y/%m/%d/", null=True, blank=True)
    extra_data = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()

    class Meta:
        verbose_name_plural = "About she"
        verbose_name = "About she"
        ordering = ["-created_at"]
        db_table = "about_she"
