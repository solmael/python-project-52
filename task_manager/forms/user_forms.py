from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from task_manager.models import Profile

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=150)
    last_name = forms.CharField(label="Фамилия", max_length=150)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            
            full_name = f"{self.cleaned_data['first_name'].strip()} {self.cleaned_data['last_name'].strip()}"
            
            if hasattr(user, 'profile'):
                user.profile.full_name = full_name
                user.profile.save()
            else:
                Profile.objects.create(user=user, full_name=full_name)


class CustomUserChangeForm(UserChangeForm):
    full_name = forms.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ('username',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.instance, 'profile'):
            self.fields['full_name'].initial = self.instance.profile.full_name
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        full_name = self.cleaned_data["full_name"].strip()
        
        if hasattr(user, 'profile'):
            user.profile.full_name = full_name
            if commit:
                user.save()
                user.profile.save()
        else:
            Profile.objects.create(user=user, full_name=full_name)
            if commit:
                user.save()
                
        return user