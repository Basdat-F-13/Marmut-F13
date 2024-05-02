from django.urls import path
from Authentication.views import *

app_name = 'Authentication'

urlpatterns = [
    path('', showLoginPage, name='login'),
    path('auth', showAuthNav, name='auth_nav'),
    path('nav', showNav, name='nav'),
]