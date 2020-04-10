from django.urls import path
from django.conf.urls import url, include
from django.views.generic import RedirectView

from registration import views

app_name = 'registration'

urlpatterns = [
    url("login", views.login, name="login"),
    url("register", views.signup, name="register"),
    url("logout", views.signup, name="logout"),
]
