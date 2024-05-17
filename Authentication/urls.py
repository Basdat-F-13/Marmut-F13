from django.urls import path
from Authentication.views import *

app_name = 'Authentication'

urlpatterns = [
    path('', showAuthNav, name='auth_nav'),
    path('login', login, name='login'),
    path('nav', showNav, name='nav'),
    path('logout', logout, name='logout'),
    path('register',showRegister, name='register'),
    path('register-user',showUserRegPage,name='register-user'),
    path('register-label',showLabelRegPage, name='register-label')
]