# Generated by Django 5.0.1 on 2024-01-17 10:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("softdesk_api", "0003_project_contributors"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="contributors",
        ),
    ]