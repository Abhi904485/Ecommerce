from django.shortcuts import render

from .forms import ContactForm


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


