from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib import messages


def index(request):
    return render(request, 'task_manager/index.html')


class CustomLoginView(LoginView):
    def form_valid(self, form):
        if self.request.session.get('account_created'):
            messages.success(self.request, "Пользователь успешно зарегистрирован")
            del self.request.session['account_created']
        
        remember_me = self.request.POST.get('remember', None)
        if remember_me:
            self.request.session.set_expiry(1209600)  # two weeks
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)