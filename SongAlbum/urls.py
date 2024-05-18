from django.urls import path
from SongAlbum.views import *

app_name = 'SongAlbum'

urlpatterns = [
    path('album-labeled', showAlbumLabel, name='show_album_label'),
    path('album', showAlbum, name='show_album'),
    path('song-labeled/<uuid:album_id>/', showSongLabel, name='show_song_label'),
    path('song/<uuid:album_id>/', showSong, name='show_song'),
    path('royalty', showRoyaltyCheck, name='royalty_check'),
    path('new-album', addAlbum, name='add_album'),
    path('new-song/<uuid:album_id>/', addSong, name='add_song'),
    path('del-song/<uuid:song_id>/<uuid:album_id>/', deleteSong, name='del_song'),
    path('del-song-labeled/<uuid:song_id>/<uuid:album_id>/', deleteSongLabel, name='del_song_label'),
    path('del-album/<uuid:album_id>/', deleteAlbum, name='del_album'),
    path('del-album-labeled/<uuid:album_id>/', deleteAlbumLabel, name='del_album_label'),
]