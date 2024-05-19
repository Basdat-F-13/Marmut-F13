from django.urls import path
from playpodcast.views import *

app_name = 'playpodcast'

urlpatterns = [
    path('playpodcast/<uuid:podcast_id>/', showplaypodcast, name='playpodcast'),
    path('listpodcast', showlistpodcast, name='listpodcast'),
]
