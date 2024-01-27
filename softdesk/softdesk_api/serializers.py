from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from users.models import CustomUser
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError


class ClassifyUserId(serializers.ModelSerializer):
    """Classify user informations if the user dont want to share his data"""

    class Meta:
        model = CustomUser
        fields = ["id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request_user = (
            self.context["request"].user if "request" in self.context else None
        )
        if request_user != instance:
            if not instance.can_data_be_shared:
                representation["id"] = "Confidential"
        return representation["id"]


class ContributorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "project"]


class ContributorSerializer(serializers.ModelSerializer):
    user = ClassifyUserId(read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user", "project"]
        read_only_fields = ("user",)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super(ContributorSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        try:
            return Contributor.objects.create(**validated_data)
        except IntegrityError:
            raise ValidationError("You are already a contributor to this project!")


class CommentSerializer(serializers.ModelSerializer):
    author = ClassifyUserId(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "issue"]
        read_only_fields = ("author", "issue")

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super(CommentSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        return Comment.objects.create(**validated_data)


class IssueSerializer(serializers.ModelSerializer):
    author = ClassifyUserId(read_only=True)
    comments = CommentSerializer(
        many=True,
        read_only=True,
        fields=(
            "id",
            "description",
            "author",
        ),
    )

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "created_time",
            "project",
            "author",
            "assigned_to",
            "comments",
        ]
        read_only_fields = ("author", "created_time")

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super(IssueSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        issue = Issue.objects.create(**validated_data)
        return issue


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True, fields=("user",))
    issues = IssueSerializer(
        many=True,
        read_only=True,
        fields=("id", "title", "description", "tag", "author", "comments"),
    )

    author = ClassifyUserId(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "type",
            "author",
            "contributors",
            "issues",
        ]
        read_only_fields = ("author", "contributors", "issues")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        project = Project.objects.create(**validated_data)
        Contributor.objects.create(user=user, project=project)
        return project

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request_user = (
            self.context["request"].user if "request" in self.context else None
        )

        is_author = request_user == instance.author
        is_contributor = (
            instance.contributors.filter(user=request_user).exists()
            if request_user and not request_user.is_anonymous
            else False
        )

        if not is_author and not is_contributor:
            limited_fields = ["id", "name", "description", "type"]
            return {field: representation[field] for field in limited_fields}

        return representation
