# Generated by Django 5.1.1 on 2024-12-01 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="questions",
            options={"verbose_name": "Questions", "verbose_name_plural": "Questions"},
        ),
        migrations.AlterModelTable(
            name="questions",
            table="Questions",
        ),
    ]
