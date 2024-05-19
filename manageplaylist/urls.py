from django.urls import path
from manageplaylist.views import *;

app_name = 'manageplaylist'

urlpatterns = [
    path('', showManagePlaylistPage, name='manage-playlist'),
    path('playlistdetail/<str:id_playlist>', showPlaylistPage, name='userplaylistdetail'),
    path('playingsong/<str:id_konten>', showPlayingSongPage, name='playingsong'),
    path('add-playlist/', add_playlist, name='add-playlist'),
    path('edit-playlist/<str:id_playlist>', edit_playlist, name='edit-playlist'),
    path('delete-playlist/<str:id_playlist>', delete_playlist, name='delete-playlist'),
    path('add-song/<str:id_playlist>', add_song, name="add-song"),
    path('add-song-to-playlist/<str:id_konten>', add_song_to_playlist, name="add-song-to-playlist"),
    path('delete-song/<str:id_playlist>/<str:id_konten>', delete_song, name='delete-song')
]