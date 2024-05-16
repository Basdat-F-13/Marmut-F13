from django.urls import path
from Authentication.views import *

app_name = 'Authentication'

urlpatterns = [
    path('', showLoginPage, name='login'),
    path('auth', showAuthNav, name='auth_nav'),
    path('nav', showNav, name='nav'),
    path('register',showRegister, name='register'),
    path('register-user',showUserRegPage,name='register-user'),
    path('register-label',showLabelRegPage, name='register-label')
]