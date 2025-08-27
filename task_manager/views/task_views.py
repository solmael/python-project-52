from django.contrib import messages
from django.contrib.auth import get_user_model
from task_manager.models import Status
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    DetailView
)

from task_manager.models import Task
from task_manager.forms import TaskForm

User = get_user_model()


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_manager/tasks/list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # filter
        status_id = self.request.GET.get('status')
        executor_id = self.request.GET.get('executor')
        label_id = self.request.GET.get('label')
        self_author = self.request.GET.get('self_author')
        
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        if label_id:
            queryset = queryset.filter(labels__id=label_id)
        if self_author == 'on':
            queryset = queryset.filter(author=self.request.user)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['self_author_checked'] = 'checked' if self.request.GET.get('self_author') == 'on' else ''
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        # context['labels'] = Label.objects.all()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/tasks/create.html'
    success_url = reverse_lazy('tasks')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно создана')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/tasks/update.html'
    success_url = reverse_lazy('tasks')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task_manager/tasks/delete.html'
    success_url = reverse_lazy('tasks')
    
    def test_func(self):
        # user == task author
        return self.get_object().author == self.request.user
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав для удаления этой задачи')
        else:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('tasks')
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Задача успешно удалена')
        return response


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_manager/tasks/detail.html'