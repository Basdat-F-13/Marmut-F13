from django.urls import path
from SongAlbum.views import *

app_name = 'SongAlbum'

urlpatterns = [
    path('album-labeled', showAlbumLabel, name='show_album_label'),
    path('album', showAlbum, name='show_album'),
    path('song-labeled/<uuid:album_id>/', showSongLabel, name='show_song_label'),
    path('song', showSong, name='show_song'),
    path('royalty', showRoyaltyCheck, name='royalty_check'),
    path('new-album', addAlbum, name='add_album'),
    path('new-song', addSong, name='add_song'),
]