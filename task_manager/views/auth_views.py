from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy


def index(request):
    return render(request, 'task_manager/index.html')


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        
        remember_me = self.request.POST.get('remember', None)
        if remember_me:
            self.request.session.set_expiry(1209600)  # two weeks
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)
    

def logout_view(request):
    messages.info(request, "Вы разлогинены")
    logout(request)
    return redirect(reverse_lazy('home'))