from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input'})
    )

    first_name = forms.CharField(
        label='Primeiro nome',
        widget=forms.TextInput(attrs={'class': 'input'}),
        required=True
    )

    password1 = forms.CharField(
        label='Palavra-passe',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input'})
    )

    password2 = forms.CharField(
        label='Confirme palavra-passe',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input'})
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'input'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'})
    )


class ResendEmailForm(forms.Form):
    email = forms.EmailField(
        label="Endereço de email", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'input'})
    )

