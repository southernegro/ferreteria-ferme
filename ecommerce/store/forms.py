from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Profile

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','last_name', 'phone_number', 'email', 'tipo']
        widgets={
            'name': forms.TextInput(attrs={'placeholder': 'Nombre...'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido...'}),
            'phone_numer': forms.TextInput(attrs={'placeholder': 'Telefono...'}),
            'email': forms.TextInput(attrs={'placeholder': 'Correo...'}),
        }