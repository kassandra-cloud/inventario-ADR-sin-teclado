import threading
from django.urls import reverse
from django.shortcuts import redirect
_user = threading.local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)
        return response

def get_current_user():
    return getattr(_user, 'value', None)
class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path

        if user.is_authenticated:
            profile = getattr(user, "profile", None)
            if profile and profile.create_by_adr:
                allow = {
                    reverse("profile_password_change"),
                    reverse("logout"),
                }
                if path not in allow and not path.startswith(("/static/", "/media/")):
                    return redirect("profile_password_change")

        return self.get_response(request)