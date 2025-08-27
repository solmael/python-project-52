from django import forms
from django.contrib.auth import get_user_model
from task_manager.models import (
    Task, 
    Status, 
    # Label, 
    )

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Имя',
            'description': 'Описание'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance.pk is None and user:
            self.instance.author = user
        
        self.fields['status'].queryset = Status.objects.all()
        
        self.fields['executor'].queryset = User.objects.all()
        
        # label
        # self.fields['labels'].queryset = Label.objects.all()