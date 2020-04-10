from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-3', 'placeholder': 'Name'}), max_length=30, required=True, help_text='As required to be printed on certificate')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-3', 'placeholder': 'USN'}), max_length=10, required=True, help_text='This will be your username')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input--style-3', 'placeholder': 'Email'}), max_length=254, required=True, help_text='CMRIT email address only.')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Password', 'class': 'input--style-3'})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'input--style-3'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-3', 'placeholder': 'USN'}), max_length=10, required=True)

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Password', 'class': 'input--style-3'})

    class Meta:
        model = User
        fields = ('username', 'password')