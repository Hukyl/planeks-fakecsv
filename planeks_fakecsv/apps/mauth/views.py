from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.views.decorators.http import require_http_methods


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse('gen:index'))
    return render(request, 'login.html')


@require_http_methods(["POST"])
def log_in(request: HttpRequest):
    q = request.POST
    user = authenticate(
        username=q.get('username'), password=q.get('password')
    )
    if user is not None:
        login(request, user)
        return redirect(reverse('gen:index'))
    return redirect(reverse('mauth:index'))


def log_out(request: HttpRequest):
    logout(request)
    return redirect(reverse('mauth:index'))
