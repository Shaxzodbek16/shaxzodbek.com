# Generated by Django 5.1.1 on 2024-12-01 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0008_alter_onetimepassword_expiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 12, 1, 9, 14, 48, 863839, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
