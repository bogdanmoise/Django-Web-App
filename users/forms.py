from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile

def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError((f"{value} is taken!"),params = {'value':value})

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators = [validate_email])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']