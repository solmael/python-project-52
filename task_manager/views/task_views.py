import django_filters
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from task_manager.forms import TaskForm
from task_manager.models import Label, Status, Task

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    self_author = django_filters.BooleanFilter(
        method='filter_self_author',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Только свои задачи'
    )
    
    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
    
    def filter_self_author(self, queryset, _, value):
        if value and hasattr(self, 'request') and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'task_manager/tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    
    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs is None:
            kwargs = {}
        kwargs['request'] = self.request
        return kwargs


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