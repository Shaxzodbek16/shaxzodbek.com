from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Img(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='problems/%Y/%m/%d/')

    def __str__(self):
        return self.title

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
        return f"Example: {self.description[:50]}"

    class Meta:
        db_table = 'Example'
        ordering = ('-id',)
        verbose_name = 'Example'
        verbose_name_plural = 'Examples'


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Topic'
        ordering = ('title',)
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'


class Hint(models.Model):
    hint = models.TextField()

    def __str__(self):
        return f"Hint: {self.hint[:50]}"

    class Meta:
        db_table = 'Hint'
        ordering = ('-id',)
        verbose_name = 'Hint'
        verbose_name_plural = 'Hints'


class Files(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='problems/files/%Y/%m/%d/')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Files'
        ordering = ('title',)
        verbose_name = 'Files'
        verbose_name_plural = 'Files'


class Theme(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Theme'
        ordering = ('title',)
        verbose_name = 'Theme'
        verbose_name_plural = 'Themes'


class Problem(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    notes = models.TextField(blank=True)
    constraints = models.TextField(blank=True)
    solution = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    images = models.ManyToManyField(Img, blank=True, related_name='problems')
    examples = models.ManyToManyField(Example, blank=True, related_name='problems')
    topics = models.ManyToManyField(Topic, blank=True, related_name='problems')
    hints = models.ManyToManyField(Hint, blank=True, related_name='problems')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    solved_users = models.ManyToManyField(User, blank=True, related_name='solved_problems')
    files = models.ManyToManyField(Files, blank=True, related_name='problems_files')
    theme = models.ManyToManyField(Theme, blank=True, related_name='theme_problems')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Problem'
        ordering = ('-created',)
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'

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


class TestCase(models.Model):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField(help_text="Input data for the test case")
    expected_output = models.TextField(help_text="Expected output for the test case")
    is_sample = models.BooleanField(default=False, help_text="Is this a sample test case visible to users?")
    order = models.PositiveIntegerField(default=1, help_text="Order of test case execution")

    class Meta:
        db_table = 'TestCase'
        ordering = ['problem', 'order']
        verbose_name = 'Test Case'
        verbose_name_plural = 'Test Cases'
        unique_together = ['problem', 'order']

    def __str__(self):
        return f"Test Case {self.order} for {self.problem.title}"


class Submission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    )

    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        # Add more languages as needed
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    execution_time = models.FloatField(null=True, blank=True, help_text="Total execution time in seconds")
    memory_usage = models.FloatField(null=True, blank=True, help_text="Peak memory usage in MB")

    class Meta:
        db_table = 'Submission'
        ordering = ['-submitted_at']
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'

    def __str__(self):
        return f"Submission by {self.user.first_name} for {self.problem.title}"


class TestResult(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='test_results')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    execution_time = models.FloatField(help_text="Execution time in seconds")
    memory_usage = models.FloatField(help_text="Memory usage in MB")
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = 'TestResult'
        ordering = ['test_case__order']
        verbose_name = 'Test Result'
        verbose_name_plural = 'Test Results'

    def __str__(self):
        return f"Test {self.test_case.order} result for submission {self.submission.id}"


class UserProblemStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_statuses')
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='user_statuses')
    is_solved = models.BooleanField(default=False)
    attempts_count = models.PositiveIntegerField(default=0)
    first_solved_at = models.DateTimeField(null=True, blank=True)
    last_attempted_at = models.DateTimeField(auto_now=True)
    best_execution_time = models.FloatField(null=True, blank=True)
    best_memory_usage = models.FloatField(null=True, blank=True)
    favorite = models.BooleanField(default=False)

    class Meta:
        db_table = 'UserProblemStatus'
        ordering = ['-last_attempted_at']
        verbose_name = 'User Problem Status'
        verbose_name_plural = 'User Problem Statuses'
        unique_together = ['user', 'problem']

    def __str__(self):
        status = "Solved" if self.is_solved else "Attempted"
        return f"{self.user.username} - {self.problem.title} ({status})"
