from .models import User
from django.utils import timezone

class UpdateLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update last_request field for the current user
            User.objects.filter(pk=request.user.pk).update(last_request=timezone.now())
        response = self.get_response(request)
        return response