from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def users(request):
    return render(request, 'users.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')