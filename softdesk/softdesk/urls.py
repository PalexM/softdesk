from django.contrib import admin
from django.urls import path, include
from users.views import UserRegistrationView, UserListView, UserAuthenticationToken

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("softdesk_api.urls")),
    path("token/", UserAuthenticationToken.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user-list"),
]
