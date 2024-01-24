from rest_framework import viewsets
from .models import Project, Contributor, Issue, Comment
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .permissions import (
    ProjectPermission,
    ContributorPermission,
    IssuePermission,
    CommentPermission,
)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "id"
    permission_classes = [ProjectPermission]
    pagination_class = LargeResultsSetPagination


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    lookup_field = "id"
    permission_classes = [ContributorPermission]
    pagination_class = LargeResultsSetPagination


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IssuePermission]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Issue.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        request.data["author"] = instance.author.id
        request.data["project"] = instance.project.id
        request.data["title"] = instance.title
        request.data["description"] = instance.description
        request.data["created_time"] = instance.created_time

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]
    pagination_class = LargeResultsSetPagination
