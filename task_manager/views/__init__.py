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

from .task_views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView
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
    'StatusDeleteView',

    # tasks
    'TaskListView',
    'TaskCreateView',
    'TaskUpdateView',
    'TaskDeleteView',
    'TaskDetailView'
]