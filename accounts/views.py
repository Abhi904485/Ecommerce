from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from Ecommerce.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from django.utils.http import is_safe_url

from accounts.forms import LoginForm, RegisterForm

User = get_user_model()


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
            'title': 'login',
            'form': form,
            'next': '/products'
    }
    next_ = request.GET.get('next')
    next_post_ = request.POST.get('next')
    redirect_path = next_ or next_post_ or context['next']
    if form.is_valid():
        username = form.cleaned_data['username'].lower()
        password = form.cleaned_data['password'].lower()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                context['form'] = LoginForm()
                context['user'] = username
                messages.success(request, "{} logged in successfully".format(username))
                return redirect(redirect_path)
        else:
            messages.error(request, "Please Enter Correct Credentials !!")

    return render(request, "login.html", context=context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
            'title': 'register',
            'form': form
    }
    if form.is_valid():
        username = form.cleaned_data['username'].lower()
        password = make_password(form.cleaned_data['password'].lower())
        email = form.cleaned_data['email'].lower()
        first_name = form.cleaned_data['first_name'].lower()
        last_name = form.cleaned_data['last_name'].lower()
        user = User.objects.create(username=username, password=password, email=email, first_name=first_name,
                                   last_name=last_name)
        context['user'] = user.username
        context['form'] = RegisterForm()
        messages.success(request, "User Registration Successful try to login with {}".format(context['user']))
        return redirect('accounts:login')
    return render(request, "register.html", context=context)


def logout_page(request):
    logout(request=request)
    return redirect(LOGOUT_REDIRECT_URL)
