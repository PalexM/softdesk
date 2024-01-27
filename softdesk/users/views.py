from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from users.models import CustomUser


class UserRegistrationView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = get_user_model()
        users = User.objects.all()
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data)


class UserAuthenticationToken(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            username = request.data.get("username")
            user = CustomUser.objects.get(username=username)
            user.last_connected = timezone.now()
            user.save()
        return response


class InactiveUsers:
    @staticmethod
    def delete_inactive_users():
        three_years_ago = timezone.now() - timedelta(days=3 * 365)

        users_to_delete = CustomUser.objects.filter(last_connected__lt=three_years_ago)
        count = users_to_delete.count()
        users_to_delete.delete()
