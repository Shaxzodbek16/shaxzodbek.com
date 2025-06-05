from django.db import models
from django.utils.text import slugify
import os


class Post(models.Model):
    title = models.CharField(max_length=100)
    content1 = models.TextField()
    image = models.ImageField(upload_to="blog/posts/%Y/%m/%d", null=True, blank=True)
    content2 = models.TextField()
    created = models.DateTimeField()
    visible = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    @property
    def next(self):
        next_article = (
            Post.objects.filter(created__lt=self.created, visible=True)
            .order_by("-created")
            .first()
        )
        return next_article

    @property
    def previous(self):
        prev_article = (
            Post.objects.filter(created__gt=self.created, visible=True)
            .order_by("created")
            .first()
        )
        return prev_article

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]
        db_table = "posts"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(
        upload_to="blog/programming_languages/%Y/%m/%d", null=True, blank=True
    )
    knowing_percentage = models.FloatField(default=0)
    started_from = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-started_from"]
        db_table = "programming_languages"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Education(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to="blog/education/%Y/%m/%d", null=True, blank=True
    )
    started_from = models.DateTimeField()
    ended_at = models.DateTimeField()
    field = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-started_from"]
        db_table = "education"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Certification(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to="blog/certificate/%Y/%m/%d", null=True, blank=True
    )
    took_at = models.DateTimeField(null=True, blank=True)

    @property
    def next(self):
        next_cert = Certification.objects.filter(id__gt=self.id).order_by("id").first()
        return next_cert

    @property
    def previous(self):
        prev_cert = Certification.objects.filter(id__lt=self.id).order_by("-id").first()
        return prev_cert

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        db_table = "certification"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Type(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        db_table = "types"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="blog/projects/%Y/%m/%d", null=True, blank=True)
    programming_languages = models.ManyToManyField(ProgrammingLanguage)
    link_to_project = models.URLField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    started_from = models.DateTimeField()
    ended_at = models.DateTimeField()
    type = models.ManyToManyField(Type)

    @property
    def next(self):
        next_project = (
            Project.objects.filter(started_from__lt=self.started_from)
            .order_by("-started_from")
            .first()
        )
        return next_project

    @property
    def previous(self):
        prev_project = (
            Project.objects.filter(started_from__gt=self.started_from)
            .order_by("started_from")
            .first()
        )
        return prev_project

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-started_from"]
        db_table = "projects"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CV(models.Model):
    file = models.FileField(upload_to="blog/cv/", null=True, blank=True)

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ["-file"]
        db_table = "cv"

    def save(self, *args, **kwargs):
        existing_cvs = CV.objects.all()
        for cv in existing_cvs:
            if cv.file:
                if os.path.isfile(cv.file.path):
                    os.remove(cv.file.path)
            cv.delete()
        self.file.name = "Muxtorov_Shaxzodbek_cv." + self.file.name.split(".")[-1]
        super().save(*args, **kwargs)

    @property
    def get_file_url(self):
        return self.file.url
