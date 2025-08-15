from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        user.profile.full_name = self.cleaned_data["full_name"]
        user.profile.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    full_name = forms.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ('username',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].initial = self.instance.profile.full_name
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile.full_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
            user.profile.save()
        return user