# Generated by Django 5.1.1 on 2024-12-17 19:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0022_alter_onetimepassword_expiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 12, 17, 19, 16, 1, 100498, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
