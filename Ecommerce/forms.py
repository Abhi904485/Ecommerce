from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
                           required=True,
                           error_messages={'required': "please enter the name"}, )

    email = forms.CharField(label="Name", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your mail'}),
                            required=True,
                            error_messages={'required': "please enter the mail"}, )

    content = forms.CharField(label="Enter content", required=True,
                              error_messages={'required': "please enter the mail"},
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control', 'placeholder': 'Enter you content here'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if 'gmail.com' not in email:
            raise forms.ValidationError("Email should be in gmail.com")
        return email


class GeneralForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
                               required=True,
                               error_messages={'required': "please enter the username"}, )

    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
                               required=True,
                               error_messages={'required': "please enter the password"}, )


class LoginForm(GeneralForm):
    pass


class RegisterForm(GeneralForm):
    password1 = forms.CharField(label="Confirm password", error_messages={'required': "please enter the password"},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Renter your password'}),
                                required=True,
                                )

    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
                                 required=True,
                                 error_messages={'required': "please enter the first name"}, )

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
                                required=True,
                                error_messages={'required': "please enter the last name"}, )

    email = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your mail'}),
                             required=True,
                             error_messages={'required': "please enter the mail"}, )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username.lower()).exists():
            raise forms.ValidationError("User Already Exists!")
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email.lower()).exists():
            raise forms.ValidationError("Email  Already Exists!")
        return email.lower()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.lower()

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name.lower()

    def clean(self):
        data = self.cleaned_data
        if data:
            password = data['password']
            password1 = data['password1']
            if password != password1:
                raise forms.ValidationError("Password should match!")
            return data
