from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

def index(request):
    return render(request, 'task_manager/index.html')

def users(request):
    return render(request, 'users.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

class UsersListView(ListView):
    model = CustomUser
    template_name = 'task_manager/users.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'task_manager/register.html'
    success_url = reverse_lazy('login')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'task_manager/user_update.html'
    success_url = reverse_lazy('users')

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'task_manager/user_delete.html'
    success_url = reverse_lazy('users')

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)