from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.forms import LabelForm
from task_manager.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'task_manager/labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'task_manager/labels/create.html'
    success_url = reverse_lazy('labels')


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'task_manager/labels/update.html'
    success_url = reverse_lazy('labels')


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'task_manager/labels/delete.html'
    success_url = reverse_lazy('labels')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = self.get_object()
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить метку, потому что она используется')
            return redirect('labels')