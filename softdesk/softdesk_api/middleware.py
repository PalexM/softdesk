# from django.utils import timezone
# from django.contrib.auth import get_user_model


# class UpdateLastConnectedUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         print("hereeeee")
#         if request.user.is_authenticated:
#             User = get_user_model()
#             user = User.objects.filter(id=request.user.id).first()
#             if user:
#                 user.last_connected = timezone.now()
#                 user.save()

#         return response
