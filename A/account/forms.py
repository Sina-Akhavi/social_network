from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterUserForm(forms.Form):
    username = forms.CharField(label='username')
    email = forms.EmailField(label='email address', widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    confirm_pass = forms.CharField(label='confirm password',
                                   widget=forms.PasswordInput(attrs={'placeholder': 'confirm'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()

        if user:
            raise ValidationError('this email already exists')
        else:
            return email

    def clean(self):
        clean_data = super().clean()
        p = clean_data.get('password')
        confirm_p = clean_data.get('confirm_pass')

        if p and confirm_p and p != confirm_p:
            raise ValidationError('password and its confirm are different!!!')

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()

        if user:
            raise ValidationError('this username already exists')
        else:
            return username


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


