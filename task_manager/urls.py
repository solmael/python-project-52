"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    CustomLoginView,
    LabelCreateView,
    LabelDeleteView,
    LabelListView,
    LabelUpdateView,
    StatusCreateView,
    StatusDeleteView,
    StatusListView,
    StatusUpdateView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    UserCreateView,
    UserDeleteView,
    UsersListView,
    UserUpdateView,
    index,
    logout_view,
)

urlpatterns = [
    #  home
    path('', index, name='home'),
    
    # users
    path(
        'users/', 
         UsersListView.as_view(), 
         name='users'
         ),
    path(
        'users/create/', 
         UserCreateView.as_view(), 
         name='user_create'
         ),
    path(
        'users/<int:pk>/update/', 
         UserUpdateView.as_view(), 
         name='user_update'
         ),
    path(
        'users/<int:pk>/delete/', 
         UserDeleteView.as_view(), 
         name='user_delete'
         ),

    # statuses
    path(
        'statuses/', 
         StatusListView.as_view(), 
         name='statuses'
         ),
    path(
        'statuses/create/', 
         StatusCreateView.as_view(), 
         name='status_create'
         ),
    path(
        'statuses/<int:pk>/update/', 
         StatusUpdateView.as_view(), 
         name='status_update'
         ),
    path(
        'statuses/<int:pk>/delete/', 
         StatusDeleteView.as_view(), 
         name='status_delete'
         ),
    
    # tasks
    path(
        'tasks/', 
        TaskListView.as_view(), 
        name='tasks'
        ),
    path(
        'tasks/create/', 
        TaskCreateView.as_view(), 
        name='task_create'
        ),
    path(
        'tasks/<int:pk>/update/', 
        TaskUpdateView.as_view(), 
        name='task_update'
        ),
    path(
        'tasks/<int:pk>/delete/', 
        TaskDeleteView.as_view(), 
        name='task_delete'
        ),
    path(
        'tasks/<int:pk>/', 
        TaskDetailView.as_view(), 
        name='task_detail'
        ),

    # labels
    path(
        'labels/', 
        LabelListView.as_view(), 
        name='labels'
        ),
    path(
        'labels/create/', 
        LabelCreateView.as_view(), 
        name='label_create'
        ),
    path(
        'labels/<int:pk>/update/', 
        LabelUpdateView.as_view(), 
        name='label_update'
        ),
    path(
        'labels/<int:pk>/delete/', 
        LabelDeleteView.as_view(), 
        name='label_delete'
        ),

    # auth
    path('login/', CustomLoginView.as_view(
        template_name='task_manager/users/login.html',
        redirect_authenticated_user=False,
        redirect_field_name='next',
        success_url='/'
    ), name='login'),
    
    path('logout/', logout_view, name='logout'),
]