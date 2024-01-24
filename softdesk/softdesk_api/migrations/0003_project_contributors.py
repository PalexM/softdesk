# Generated by Django 5.0.1 on 2024-01-17 10:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("softdesk_api", "0002_remove_comment_uuid"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="contributors",
            field=models.ManyToManyField(
                related_name="contributed_projects", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]