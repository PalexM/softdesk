from rest_framework import permissions
from .models import Project, Contributor, Issue
from rest_framework.exceptions import PermissionDenied


from rest_framework import permissions


def is_contributor(user, project):
    """Return True of False if user is contributor of a project"""
    contributor = Contributor.objects.filter(user_id=user, project_id=project).exists()
    return contributor


class ProjectPermission(permissions.BasePermission):
    """
    Custom permission to only allow authors of a project to edit or delete it
    Only connected users are allow to see some of data
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ContributorPermission(permissions.BasePermission):
    """
    Custom permission to allow any authenticated user to become a contributor.
    Only connected users are allow to see some of data
    Only contributors of a project can access the project and its related resources (issues and comments).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.project.contributors.filter(user=request.user).exists()


class IssuePermission(permissions.BasePermission):
    """
    Custom permission to:
    - Allow any authenticated user to view all issues if is a contributor.
    - Only connected users are allow to see some of data
    - Allow only the issue author to modify title, description, and to assign the issue to a project contributor.
    - Allow only project contributors to modify 'tag', 'priority', and 'status'.
    - Ensure that an issue can only be assigned to a project contributor.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        else:
            raise PermissionDenied(detail="Not connected")

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        elif is_contributor(request.user, obj.project.id):
            if request.method != "DELETE":
                if (obj.assigned_to.id, obj.project.id):
                    return True
                else:
                    raise PermissionDenied(
                        detail="Assigned user is not a contributor of project!"
                    )
            else:
                raise PermissionDenied(detail="Only author can delete a project!")
        else:
            raise PermissionDenied(detail="User is not a contributor of project!")


class CommentPermission(permissions.BasePermission):
    """
    Custom permission to only allow contributors of the project associated with an issue to add a comment.
    Only connected users are allow to see some of data
    Only the comment author or the issue author can delete the comment.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == "POST":
            issue_id = request.data.get("issue")
            if issue_id is None:
                return False
            issue = Issue.objects.get(id=issue_id)
            if is_contributor(request.user, issue.project.pk):
                return True
            return False
        elif request.method == "PUT" or "PATCH":
            return request.user and request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        # Check if the request is a safe method (GET, HEAD, OPTIONS)
        if request.method == "PUT" or "PATCH":
            if request.user == obj.author:
                return True
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the request user is the author of the comment or the author of the associated issue
        return obj.author == request.user or obj.issue.author == request.user
