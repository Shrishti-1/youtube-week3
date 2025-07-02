from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.http import FileResponse
from pathlib import Path
import os
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect


tokens = {}  # Simulated token store


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

            token = f"{user.username}_123"
            tokens[token] = user.username

            messages.success(request, "Account created successfully! Please verify your account.")

            return redirect(f'/verify/{token}') 
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def verify_view(request, token):
    username = tokens.get(token)
    if username:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()

        messages.success(request, "✅ Account Verified Successfully! You can now login.")
        return redirect('login')

    # Invalid token case
    return render(request, 'verify.html', {'error': '❌ Invalid or expired verification link.'})

def login_view(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pword = request.POST['password']
        user = authenticate(username=uname, password=pword)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})
