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



