from .auth_views import CustomLoginView, index, logout_view
from .user_views import (
    UserCreateView,
    UserDeleteView,
    UsersListView,
    UserUpdateView,
)


from .status_views import (
    StatusListView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView
)


__all__ = [
    # users
    'UsersListView',
    'UserCreateView',
    'UserUpdateView',
    'UserDeleteView',
    
    # auth
    'index',
    'CustomLoginView',
    'logout_view',
    
    # statuses
    'StatusListView',
    'StatusCreateView',
    'StatusUpdateView',
    'StatusDeleteView'
]