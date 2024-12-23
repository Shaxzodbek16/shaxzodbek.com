# Generated by Django 5.1.1 on 2024-11-19 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="blog/articles/%Y/%m/%d"
                    ),
                ),
                ("body", models.TextField()),
                ("created", models.DateTimeField()),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "slug",
                    models.SlugField(
                        blank=True, default="", max_length=255, null=True, unique=True
                    ),
                ),
                ("telegram", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Article",
                "verbose_name_plural": "Articles",
                "db_table": "articles",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Author",
                "verbose_name_plural": "Authors",
                "db_table": "author",
                "ordering": ["-first_name"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "db_table": "category",
                "ordering": ["-name"],
            },
        ),
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("who_is_it", models.CharField(max_length=255)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "verbose_name": "Match",
                "verbose_name_plural": "Matches",
                "db_table": "matches",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="ProgrammingLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "ProgrammingLanguage",
                "verbose_name_plural": "ProgrammingLanguages",
                "db_table": "programmingLanguage",
                "ordering": ["-name"],
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("url", models.URLField()),
                ("created", models.DateTimeField()),
                ("thumbnail", models.ImageField(upload_to="blog/video/%Y/%m/%d")),
            ],
            options={
                "verbose_name": "Video",
                "verbose_name_plural": "Videos",
                "db_table": "video",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Connection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("picture", models.ImageField(upload_to="blog/connection/%Y/%m/%d")),
                ("birth_date", models.DateField()),
                ("job_title", models.CharField(blank=True, max_length=255, null=True)),
                ("met_address", models.TextField()),
                ("home_address", models.TextField(blank=True, null=True)),
                ("met_at", models.DateTimeField()),
                ("listed", models.BooleanField(default=True)),
                (
                    "who_for_me",
                    models.ManyToManyField(related_name="who_me", to="blog.match"),
                ),
            ],
            options={
                "verbose_name": "Connection",
                "verbose_name_plural": "Connections",
                "db_table": "connections",
                "ordering": ["-birth_date"],
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("purpose", models.CharField(max_length=255)),
                ("picture", models.ImageField(upload_to="blog/book/%Y/%m/%d")),
                ("book", models.FileField(upload_to="blog/files/book/%Y/%m/%d")),
                (
                    "author",
                    models.ManyToManyField(
                        related_name="books_author", to="blog.author"
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(
                        related_name="books_categories", to="blog.category"
                    ),
                ),
                (
                    "programming_language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="blog.programminglanguage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Book",
                "verbose_name_plural": "Books",
                "db_table": "book",
                "ordering": ["-title"],
            },
        ),
    ]
