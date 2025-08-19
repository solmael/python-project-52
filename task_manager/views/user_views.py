from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class UsersListView(ListView):
    model = User
    template_name = 'task_manager/users/users.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'task_manager/users/register.html'
    
    def get_success_url(self):
        return reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'task_manager/user_update.html'
    success_url = reverse_lazy('users')
    
    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'task_manager/user_delete.html'
    success_url = reverse_lazy('users')
    
    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)