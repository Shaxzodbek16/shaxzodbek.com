from django.db import models
from slugify import slugify


class Math(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=100)
    image = models.ImageField(upload_to="api/math/%Y/%m/%d", null=True, blank=True)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100, null=True, blank=True)
    option3 = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    taken_book = models.CharField(max_length=100, null=True, blank=True)
    theme = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.question[:10]} --- answer is {self.answer[:10]}"

    def __eq__(self, other):
        return self.question == other.question

    def __repr__(self):
        return f"{self.__class__.__name__} {self.__str__()}"

    class Meta:
        db_table = "Math"
        verbose_name_plural = "Maths"
        verbose_name = "Math"
        unique_together = ("option1", "option2", "option3", "answer")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
        if self.slug != slugify(self.question):
            original_slug = slugify(self.question)
            slug = original_slug
            num = 1
            while Math.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
