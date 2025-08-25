from .auth_views import CustomLoginView, index
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
    
    # statuses
    'StatusListView',
    'StatusCreateView',
    'StatusUpdateView',
    'StatusDeleteView'
]