from django.urls import path
from playpodcast.views import *

app_name = 'playpodcast'

urlpatterns = [
    path('playpodcast', showplaypodcast, name='playpodcast'),
]
