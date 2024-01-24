from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

from .models import Project, Issue, Comment, Contributor


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "id")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "date_of_birth",
                    "last_connected",
                    "can_data_be_shared",
                    "can_be_contacted",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "author")
    fieldsets = ((None, {"fields": ("name", "description", "type", "author")}),)


admin.site.register(Project, ProjectAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "id")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "tag",
                    "priority",
                    "status",
                    "project",
                    "author",
                    "assigned_to",
                )
            },
        ),
    )


admin.site.register(Issue, IssueAdmin)


class ContribuitorAdmin(admin.ModelAdmin):
    list_display = ("user", "project")
    fieldsets = (
        (
            None,
            {"fields": ("user", "project")},
        ),
    )


admin.site.register(Contributor, ContribuitorAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("description", "author")
    fieldsets = (
        (
            None,
            {"fields": ("description", "author", "issue")},
        ),
    )


admin.site.register(Comment, CommentAdmin)
