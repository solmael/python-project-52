def person(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
    return None