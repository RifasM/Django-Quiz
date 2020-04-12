from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-3', 'placeholder': 'Name'}),
                                 max_length=30, required=True, help_text='As required to be printed on certificate')
    usn = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input--style-3', 'placeholder': 'USN', 'pattern': '1(cr|CR)\d{2}\w{2}\d{3}'}), max_length=10,
        required=True)
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'input--style-3', 'placeholder': 'Email', 'pattern': '[\w\.]{4}\d{2}\w{2}@cmrit.ac.in'}),
        max_length=254, required=True, help_text='CMRIT email address only. Will be used for verification')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Password', 'class': 'input--style-3'})
        self.fields['password2'].widget = PasswordInput(
            attrs={'placeholder': 'Confirm Password', 'class': 'input--style-3'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'usn', 'password1', 'password2')


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-3', 'placeholder': 'Email', 'pattern': '[\w\.]{4}\d{2}\w{2}@cmrit.ac.in'}),
                               max_length=10, required=True)

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Password', 'class': 'input--style-3'})

    class Meta:
        model = User
        fields = ('username', 'password')
