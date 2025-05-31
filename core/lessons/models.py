from django.db import models
from django.utils.text import slugify


class AbstractBaseModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_up = models.DateTimeField(auto_now=True)

    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return f"{self.__class__.__name__}({self.title})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title})"

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
