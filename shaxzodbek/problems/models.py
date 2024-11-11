from django.db import models
from slugify import slugify


class Img(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='problems/%Y/%m/%d/')

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return self.title == other.title

    def __repr__(self):
        return f"{self.__str__()} {self.__class__.__name__}"

    class Meta:
        db_table = 'Img'
        ordering = ('title',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Example(models.Model):
    input = models.TextField()
    output = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"{self.input[:10]} {self.output[:10]}"

    def __repr__(self):
        return f"{self.__str__()} {self.__class__.__name__}"

    def __eq__(self, other):
        return self.input == other.input and self.output == other.output and self.description == other.description

    class Meta:
        db_table = 'Example'
        ordering = '-id'
        verbose_name = 'Example'
        verbose_name_plural = 'Examples'


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.__str__()} {self.__class__.__name__}"

    def __eq__(self, other):
        return self.title == other.title and self.description == other.description

    class Meta:
        db_table = 'Topic'
        ordering = '-id'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'


class Hint(models.Model):
    hint = models.TextField()

    def __str__(self):
        return self.hint[:10]

    def __repr__(self):
        return f"{self.__str__()} {self.__class__.__name__}"

    def __eq__(self, other):
        return self.hint == other.hint and self.hint == other.hint

    class Meta:
        db_table = 'Hint'
        ordering = '-id'
        verbose_name = 'Hint'
        verbose_name_plural = 'Hints'


class Problem(models.Model):
    difficulties = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    notes = models.TextField()
    constraints = models.TextField()  # limits
    solution = models.TextField()
    difficulty = models.CharField(max_length=20, choices=difficulties)
    images = models.ManyToManyField(Img, blank=True, null=True, related_name='problem_images')
    examples = models.ManyToManyField(Example, blank=True, null=True, related_name='problem_examples')
    topics = models.ManyToManyField(Topic, blank=True, null=True, related_name='problem_topics')
    hints = models.ManyToManyField(Hint, blank=True, null=True, related_name='problem_hints')
    slug = models.SlugField(populate_from='title', unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:10]

    def __repr__(self):
        return f"{self.__str__()} {self.__class__.__name__}"

    def __eq__(self, other):
        return self.title == other.title and self.description == other.description and self.solution == other.solution

    class Meta:
        db_table = 'Problem'
        ordering = '-id'
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            original_slug = slugify(self.title)
            slug = original_slug
            num = 1
            while Problem.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
