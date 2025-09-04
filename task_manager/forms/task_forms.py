from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import (
    Label,
    Status,
    Task,
)

User = get_user_model()


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username


class TaskForm(forms.ModelForm):
    executor = UserChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Исполнитель',
    )
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'labels': 'Метки'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance.pk is None and user:
            self.instance.author = user
        
        self.fields['status'].queryset = Status.objects.all()
        
        self.fields['executor'].queryset = User.objects.all()
        
        self.fields['labels'].queryset = Label.objects.all()