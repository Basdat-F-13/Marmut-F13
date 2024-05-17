from django.shortcuts import render
from .models import User, Playlist

def showdashboard(request):
    users = User.objects.all()
    playlists = Playlist.objects.all()
    return render(request, 'dashboard.html', {'users': users, 'playlists': playlists})
