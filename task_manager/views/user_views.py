from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
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
        self.request.session['account_created'] = True
        return reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return response


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'task_manager/users/update.html'
    success_url = reverse_lazy('users')
    
    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request, 
                "У вас нет прав для изменения другого пользователя."
            )
            return redirect('users')
        else:
            messages.error(
                self.request, 
                "Вы не авторизованы! Пожалуйста, выполните вход."
            )
            return redirect('login')
    
    def form_valid(self, form):
        self.request.session_update = bool(form.cleaned_data.get('password1'))
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'task_manager/users/delete.html'
    success_url = reverse_lazy('users')
    
    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request, 
                "У вас нет прав для изменения"
            )
            return redirect('users')
        else:
            messages.error(
                self.request, 
                "Вы не авторизованы! Пожалуйста, выполните вход."
            )
            return redirect('login')
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        
        if user.author_tasks.exists() or user.executor_tasks.exists():
            messages.error(
                request, 
                'Невозможно удалить пользователя, потому что он используется'
            )
            return redirect('users')
        
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, "Пользователь успешно удален")
        return reverse_lazy('users')
    
    def delete(self, request, *args, **kwargs):
        username = self.get_object().username
        request.session['deleted_username'] = username
        
        if request.user == self.get_object():
            request.session['self_deleted'] = True
        
        return super().delete(request, *args, **kwargs)
