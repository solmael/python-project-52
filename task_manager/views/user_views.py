from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

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
        self.request.session['account_created'] = True
        return reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'task_manager/users/update.html'
    success_url = reverse_lazy('users')
    
    def test_func(self):
        # Проверяем, что пользователь пытается изменить свой профиль
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # Пользователь авторизован, но пытается изменить чужой профиль
            messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
            return redirect('users')
        else:
            # Пользователь не авторизован
            messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
            return super().handle_no_permission()


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'task_manager/user_delete.html'
    success_url = reverse_lazy('users')
    
    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)