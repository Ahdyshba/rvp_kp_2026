from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return render(request, 'users/login.html', {'access_token': access_token})
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь уже существует')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Регистрация успешна. Войдите.')
            return redirect('login')
    return render(request, 'users/register.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/profile.html')

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'username': request.user.username,
            'email': request.user.email,
        })