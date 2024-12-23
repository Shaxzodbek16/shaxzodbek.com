# Generated by Django 5.1.1 on 2024-12-01 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutMe",
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
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="cv/aboutMe/%Y/%m/%d/"
                    ),
                ),
                ("extra_data", models.TextField(blank=True, null=True)),
                ("location", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField()),
            ],
            options={
                "verbose_name": "About Me",
                "verbose_name_plural": "About Me",
                "db_table": "about_me",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CVImages",
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
                ("image", models.ImageField(upload_to="cv/cvImages/%Y/%m/%d/")),
            ],
            options={
                "verbose_name": "CV Image",
                "verbose_name_plural": "CV Images",
                "db_table": "cv_images",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Technology",
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
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Technology",
                "verbose_name_plural": "Technologies",
                "db_table": "technologies",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="CV",
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
                (
                    "file",
                    models.FileField(
                        blank=True, null=True, upload_to="cv/cvFiles/%Y/%m/%d/"
                    ),
                ),
                ("path", models.URLField(blank=True, null=True)),
                (
                    "project_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField()),
                ("is_working", models.BooleanField(default=False)),
                (
                    "picture",
                    models.ManyToManyField(
                        related_name="cv_pictures", to="blog.cvimages"
                    ),
                ),
                (
                    "technologies",
                    models.ManyToManyField(
                        related_name="cv_pictures", to="blog.technology"
                    ),
                ),
            ],
            options={
                "verbose_name": "CV",
                "verbose_name_plural": "CVs",
                "db_table": "cvs",
                "ordering": ["-created_at"],
            },
        ),
    ]
