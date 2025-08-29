from .auth_views import CustomLoginView, index, logout_view
from .label_views import (
    LabelCreateView,
    LabelDeleteView,
    LabelListView,
    LabelUpdateView,
)
from .status_views import (
    StatusCreateView,
    StatusDeleteView,
    StatusListView,
    StatusUpdateView,
)
from .task_views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)
from .user_views import (
    UserCreateView,
    UserDeleteView,
    UsersListView,
    UserUpdateView,
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

    # labels
    'LabelListView', 
    'LabelCreateView', 
    'LabelUpdateView', 
    'LabelDeleteView',
    
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