from django.db import models
from django.conf import settings
import uuid


class Project(models.Model):
    TYPE_CHOICES = [
        ("BACK", "Back-End"),
        ("FRONT", "Front-End"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # You can add more fields such as role or permission type if needed


class Issue(models.Model):
    PRIORITY_CHOICES = [("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")]
    TAG_CHOICES = [("BUG", "Bug"), ("FEATURE", "Feature"), ("TASK", "Task")]
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("INPROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.CharField(max_length=7, choices=TAG_CHOICES)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="TODO")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    # Optionally, you can add a field for assigned user if issues are to be assigned


class Comment(models.Model):
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
