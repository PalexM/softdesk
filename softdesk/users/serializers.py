# users/serializers.py
from rest_framework import serializers
from datetime import datetime
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "password", "email", "date_of_birth")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_date_of_birth(self, value):
        try:
            # Parse the date from dd/mm/yyyy format
            parsed_date = datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError:
            raise serializers.ValidationError(
                "Date of birth must be in DD/MM/YYYY format."
            )

        # Check if age is at least 15
        today = datetime.today().date()
        age = (
            today.year
            - parsed_date.year
            - ((today.month, today.day) < (parsed_date.month, parsed_date.day))
        )
        if age < 15:
            raise serializers.ValidationError(
                "Users must be at least 15 years old to register."
            )

        return parsed_date

    def create(self, validated_data):
        # Create the user
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            date_of_birth=validated_data["date_of_birth"],  # Save the parsed date
        )
        return user
