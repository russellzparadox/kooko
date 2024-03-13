from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import SignUpForm, LoginForm


# Create your views here.


class Index(View):
    def get(self, request):
        return render(request, 'accounts/index.html', )


class RedirectIndex(View):
    def get(self, request):
        return redirect('/index/')


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
