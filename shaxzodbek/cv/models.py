from django.db import models
from slugify import slugify


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Technologies'
        verbose_name = 'Technology'
        ordering = ['name']
        db_table = 'technologies'


class CVImages(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cv/cvImages/%Y/%m/%d/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'CV Images'
        verbose_name = 'CV Image'
        ordering = ['name']
        db_table = 'cv_images'


class CV(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ManyToManyField(CVImages, related_name='cv_pictures')
    file = models.FileField(upload_to='cv/cvFiles/%Y/%m/%d/', blank=True, null=True)
    technologies = models.ManyToManyField(Technology, related_name='cv_pictures')
    path = models.URLField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
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
        verbose_name_plural = 'CVs'
        verbose_name = 'CV'
        ordering = ["-created_at"]
        db_table = 'cvs'


class AboutMe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='cv/aboutMe/%Y/%m/%d/', null=True, blank=True)
    extra_data = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'About Me'
        verbose_name = 'About Me'
        ordering = ["-created_at"]
        db_table = 'about_me'
