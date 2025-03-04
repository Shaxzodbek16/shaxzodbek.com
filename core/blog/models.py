from django.db import models
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=100)
    content1 = models.TextField()
    image = models.ImageField(upload_to='blog/articles/%Y/%m/%d', null=True, blank=True)
    content2 = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        db_table = 'articles'

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='blog/programming_languages/%Y/%m/%d', null=True, blank=True)
    started_from = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-started_from']
        db_table = 'programming_languages'

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Education(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='blog/education/%Y/%m/%d', null=True, blank=True)
    started_from = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)
    field = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-started_from']
        db_table = 'education'

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Certification(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='blog/certificate/%Y/%m/%d', null=True, blank=True)
    took_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        db_table = 'certification'

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='blog/projects/%Y/%m/%d', null=True, blank=True)
    programming_languages = models.ManyToManyField(ProgrammingLanguage)
    link_to_project = models.URLField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    started_from = models.DateTimeField()
    ended_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-started_from']
        db_table = 'projects'

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
