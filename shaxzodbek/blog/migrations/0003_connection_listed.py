# Generated by Django 5.1.1 on 2024-10-14 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_connection_met_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='listed',
            field=models.BooleanField(default=True),
        ),
    ]