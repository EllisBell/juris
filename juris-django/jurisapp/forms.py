from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Palavra-passe',
        strip=False,
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirme palavra-passe',
        strip=False,
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = User
        fields = ['email']
