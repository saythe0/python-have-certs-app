from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib. auth.decorators import login_required
from django.contrib import messages
from . forms import CustomUserCreationForm, CustomAuthenticationForm, ApplicationForm, ReviewForm
from .models import Application, Review

def home(request):
    return render(request, 'main/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request. method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.user. is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def applications_list(request):
    applications = Application. objects.filter(user=request. user)
    return render(request, 'main/applications_list.html', {'applications': applications})

@login_required
def application_create(request):
    if request. method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form. save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('applications_list')
    else:
        form = ApplicationForm()
    return render(request, 'main/application_create.html', {'form': form})

@login_required
def review_create(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    
    # Проверяем, что обучение завершено
    if application.status != 'completed':
        messages.error(request, 'Отзыв можно оставить только после завершения обучения')
        return redirect('applications_list')
    
    # Проверяем, что отзыв еще не оставлен
    if hasattr(application, 'review'):
        messages.error(request, 'Вы уже оставили отзыв на эту заявку')
        return redirect('applications_list')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form. is_valid():
            review = form.save(commit=False)
            review.application = application
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('applications_list')
    else:
        form = ReviewForm()
    
    return render(request, 'main/review_create.html', {
        'form': form,
        'application': application
    })