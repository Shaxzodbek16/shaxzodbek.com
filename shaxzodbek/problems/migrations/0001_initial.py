# Generated by Django 5.1.1 on 2024-11-14 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Example",
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
                ("input", models.TextField()),
                ("output", models.TextField()),
                ("description", models.TextField()),
            ],
            options={
                "verbose_name": "Example",
                "verbose_name_plural": "Examples",
                "db_table": "Example",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="Hint",
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
                ("hint", models.TextField()),
            ],
            options={
                "verbose_name": "Hint",
                "verbose_name_plural": "Hints",
                "db_table": "Hint",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="Img",
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
                ("image", models.ImageField(upload_to="problems/%Y/%m/%d/")),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
                "db_table": "Img",
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Topic",
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
                ("description", models.TextField()),
            ],
            options={
                "verbose_name": "Topic",
                "verbose_name_plural": "Topics",
                "db_table": "Topic",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="Problem",
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
                ("description", models.TextField()),
                ("notes", models.TextField()),
                ("constraints", models.TextField()),
                ("solution", models.TextField()),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("easy", "Easy"),
                            ("medium", "Medium"),
                            ("hard", "Hard"),
                        ],
                        max_length=20,
                    ),
                ),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "examples",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="problem_examples",
                        to="problems.example",
                    ),
                ),
                (
                    "hints",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="problem_hints",
                        to="problems.hint",
                    ),
                ),
                (
                    "images",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="problem_images",
                        to="problems.img",
                    ),
                ),
                (
                    "topics",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="problem_topics",
                        to="problems.topic",
                    ),
                ),
            ],
            options={
                "verbose_name": "Problem",
                "verbose_name_plural": "Problems",
                "db_table": "Problem",
                "ordering": ("-id",),
            },
        ),
    ]