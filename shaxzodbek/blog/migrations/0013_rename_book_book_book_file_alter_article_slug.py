# Generated by Django 5.1.1 on 2024-12-17 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0012_book_download_count_alter_article_slug"),
    ]

    operations = [
        migrations.RenameField(
            model_name="book",
            old_name="book",
            new_name="book_file",
        ),
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(
                blank=True,
                default="445b8310-77ad-4fa0-b27d-c881bf003102",
                max_length=255,
                null=True,
                unique=True,
            ),
        ),
    ]
