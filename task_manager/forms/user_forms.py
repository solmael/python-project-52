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
    password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput,
        required=False,
        help_text="Оставьте пустым, если не хотите менять пароль."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        required=False
    )
    
    first_name = forms.CharField(label="Имя", max_length=150)
    last_name = forms.CharField(label="Фамилия", max_length=150)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        
        if commit:
            user.save()
            
            full_name = f"{user.first_name.strip()} {user.last_name.strip()}"
            if hasattr(user, 'profile'):
                user.profile.full_name = full_name
                user.profile.save()
                
        return user