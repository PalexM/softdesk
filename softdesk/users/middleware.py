from datetime import datetime
from users.views import InactiveUsers


class DailyTaskMiddleware:
    """Run daily task in order to delete inactive users according to RGPD"""

    last_run = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_date = datetime.now().date()
        print(DailyTaskMiddleware.last_run)
        if DailyTaskMiddleware.last_run != current_date:
            self.inactive_user()
            DailyTaskMiddleware.last_run = current_date

        response = self.get_response(request)
        return response

    def inactive_user(self):
        InactiveUsers.delete_inactive_users()
        return
