# Generated by Django 5.1.1 on 2024-11-22 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "telegrambot",
            "0004_remove_telegramuser_bio_remove_telegramuser_is_bot_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="commands",
            name="response",
        ),
    ]
