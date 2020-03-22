from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input'})
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
        fields = ['email']

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'input'})
    )

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input'}
))


