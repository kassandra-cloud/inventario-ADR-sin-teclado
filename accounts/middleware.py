import threading

_user = threading.local()

class AccountsCurrentUserMiddleware:
    """
    Middleware para capturar el usuario actual en la app de accounts.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)
        return response

def get_current_user_accounts():
    """
    Obtiene el usuario actual almacenado por este middleware.
    """
    return getattr(_user, 'value', None)
