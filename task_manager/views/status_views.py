from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

from django.db.models.deletion import ProtectedError
from task_manager.models import Status
from task_manager.forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'task_manager/statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'task_manager/statuses/create.html'
    success_url = reverse_lazy('statuses')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'task_manager/statuses/update.html'
    success_url = reverse_lazy('statuses')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменен')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'task_manager/statuses/delete.html'
    success_url = reverse_lazy('statuses')
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Статус используется в задачах')
            return redirect('statuses')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.get_object()
        return context