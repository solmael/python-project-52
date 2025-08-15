from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms.user_forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model


User = get_user_model()
def index(request):
    return render(request, 'task_manager/index.html')

def users(request):
    return render(request, 'users.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

class UsersListView(ListView):
    model = User
    template_name = 'task_manager/users.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'task_manager/register.html'
    success_url = reverse_lazy('login')

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