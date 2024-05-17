from django.urls import path, re_path
from managepod.views import *

app_name = 'managepod'

urlpatterns = [
    path('managepod', showmanagepod, name='managepod'),
    re_path(r'^list/(?P<podcast_id>[0-9a-f-]+)/$', showlist, name='list'),
    path('createpod', showcreatepod, name='createpod'),
    re_path(r'^addepisode/(?P<podcast_id>[0-9a-f-]+)/$', showaddepisode, name='addepisode'),
    re_path(r'^deletepodcast/(?P<podcast_id>[0-9a-f-]+)/$', delete_podcast, name='delete_podcast'),
    re_path(r'^deleteepisode/(?P<episode_id>[0-9a-f-]+)/(?P<podcast_id>[0-9a-f-]+)/$', delete_episode, name='delete_episode'),
]
