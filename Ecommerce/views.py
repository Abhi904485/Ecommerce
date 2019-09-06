from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from Ecommerce.forms import RegisterForm
from .forms import ContactForm, LoginForm

User = get_user_model()


def home_page(request):
    context = {
        'title': 'home'
    }
    return render(request, "home.html", context=context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    context = {
        'title': 'contact',
        'form': form
    }
    if form.is_valid():
        data = form.cleaned_data
        print(data)
        context['form'] = ContactForm()

    return render(request, "contact.html", context=context)


def about_page(request):
    context = {
        'title': 'about'
    }
    return render(request, "about.html", context=context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'title': 'login',
        'form': form
    }
    if form.is_valid():
        username = form.cleaned_data['username'].lower()
        password = form.cleaned_data['password'].lower()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            context['form'] = LoginForm()
            context['user'] = username
            messages.success(request, "{} logged in successfully".format(username))
            return redirect('products:list')
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
        return redirect('login')
    return render(request, "register.html", context=context)


def logout_page(request):
    logout(request=request)
    return redirect('login')
