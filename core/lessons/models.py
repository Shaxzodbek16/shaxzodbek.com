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


class Topic(AbstractBaseModel):
    image = models.ImageField(upload_to="lessons/topics/%Y/%m/%d", null=True, blank=True)

    class Meta:
        db_table = "topics"
        verbose_name = "Topic"
        verbose_name_plural = "Topics"


class StepsOfLesson(AbstractBaseModel):
    code = models.TextField()
    image = models.ImageField(upload_to="lessons/steps/%Y/%m/%d", null=True, blank=True)

    class Meta:
        db_table = "steps_of_lessons"
        verbose_name = "Step of Lesson"
        verbose_name_plural = "Steps of Lessons"


class Lesson(AbstractBaseModel):
    thumbnail = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(blank=True, null=True)

    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)

    is_published = models.BooleanField(default=False)

    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, related_name='lessons')
    steps = models.ManyToManyField(StepsOfLesson, related_name='lessons')

    class Meta:
        db_table = "lessons"
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def add_like(self):
        self.likes += 1
        self.save()
        return self.likes

    def remove_like(self):
        if self.likes > 0:
            self.likes -= 1
        self.save()
        return self.likes

    def add_dislike(self):
        self.dislikes += 1
        self.save()
        return self.dislikes

    def remove_dislike(self):
        if self.dislikes > 0:
            self.dislikes -= 1
        self.save()
        return self.dislikes
