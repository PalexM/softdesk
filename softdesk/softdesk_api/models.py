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

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name="contributors", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project"], name="unique_contributor_project"
            )
        ]


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
    project = models.ForeignKey(
        Project, related_name="issues", on_delete=models.CASCADE
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, related_name="comments", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
