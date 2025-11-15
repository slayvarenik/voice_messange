from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

def index(request):
    context = {
        'title': 'Голосовой Календарь - Управляйте расписанием голосом'
        }
    return render(request, 'main/index.html', context)


def login(request):
    next_url = request.GET.get('next', '/user/')
    
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
        next_url = '/user/'
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next_url_post = request.POST.get('next') or request.GET.get('next', '/user/')

            if url_has_allowed_host_and_scheme(next_url_post, allowed_hosts=request.get_host()):
                next_url = next_url_post
            else:
                next_url = '/user/'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    

    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
    
    return render(request, 'main/login.html', {'form': form, 'next_url': next_url})

def register(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            tariff = request.POST.get('tariff', 'trial')
            messages.success(request, f'Аккаунт создан успешно! Войдите в систему.')
            return redirect('/login/')
    else:
        form = UserCreationForm()
    
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
    
    return render(request, 'main/register.html', {'form': form})

def user(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Пожалуйста, войдите в систему для доступа к календарю.')
        return redirect('/login/?next=/user/')

    context = {
        'user': request.user,
        'username': request.user.username,
        'user_email': request.user.email if request.user.email else ''
    }
    return render(request, 'events/user.html', context)


def events(request):
    return render(request, 'events/events.html')

def logout(request):

    auth_logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('/')
