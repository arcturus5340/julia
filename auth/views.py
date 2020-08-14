from django.shortcuts import render


def login(request):
    return render(request, 'index.html', {})


def login_handler(request):
    return render(request, 'login_form.html', {})


def registration_handler(request):
    return render(request, 'registration_form.html', {})


def reset_password_handler(request):
    return render(request, 'reset_password_form.html', {})
