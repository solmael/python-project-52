from .auth_views import CustomLoginView, index
from .user_views import (
    UserCreateView,
    UserDeleteView,
    UsersListView,
    UserUpdateView,
)

__all__ = [
    'index',
    'CustomLoginView',
    'UsersListView',
    'UserCreateView',
    'UserUpdateView',
    'UserDeleteView'
]