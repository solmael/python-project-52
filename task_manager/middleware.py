from django.contrib.auth import update_session_auth_hash


class SessionUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(request, 'session_update') and request.session_update:
            update_session_auth_hash(request, request.user)
            request.session_update = False
        return None