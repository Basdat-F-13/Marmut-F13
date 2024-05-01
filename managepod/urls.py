from django.urls import path
from managepod.views import *

app_name = 'managepod'

urlpatterns = [
    path('managepod', showmanagepod, name='managepod'),
    path('list', showlist, name='list'),
    path('createpod', showcreatepod, name='createpod'),
    path('addepisode', showaddepisode, name='addepisode'),
]
