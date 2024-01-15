from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model


class UserRegistrationView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
