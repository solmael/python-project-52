from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from task_manager.models import Profile

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    def save(self, commit=True):
        user = super().save(commit=commit)
        
        if commit:
            full_name = f"{user.first_name.strip()} {user.last_name.strip()}"
            
            if hasattr(user, 'profile'):
                user.profile.full_name = full_name
                user.profile.save()
            else:
                Profile.objects.create(user=user, full_name=full_name)
                
        return user


class CustomUserChangeForm(UserChangeForm):
    full_name = forms.CharField(max_length=255, label="Полное имя")
    
    class Meta:
        model = User
        fields = ('username',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.instance, 'profile'):
            self.fields['full_name'].initial = self.instance.profile.full_name
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        
        if commit:
            full_name = self.cleaned_data["full_name"].strip()
            
            if hasattr(user, 'profile'):
                user.profile.full_name = full_name
                user.profile.save()
            else:
                Profile.objects.create(user=user, full_name=full_name)
                
        return user