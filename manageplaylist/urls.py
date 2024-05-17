from django.urls import path
from manageplaylist.views import *;

app_name = 'manageplaylist'

urlpatterns = [
    path('', showManagePlaylistPage, name='manageplaylist'),
    path('playlistdetail/', showPlaylistPage, name='userplaylistdetail'),
    path('playingsong/', showPlayingSongPage, name='playingsong')
]