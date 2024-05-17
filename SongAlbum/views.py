from django.shortcuts import render

# Create your views here.
def showAlbumLabel(request):
    context = {
        'show_navbar' : True,
        'user' : False,
        'artist' : False,
        'songwriter' : False,
        'podcast' : False,
        'label' : True
    }
    return render(request, "manageAlbumLabel.html", context)

def showAlbum(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, "manageAlbum.html", context)

def showSongLabel(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, "manageSongLabel.html", context)

def showSong(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, "manageSong.html", context)

def showRoyaltyCheck(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, "royaltyCheck.html", context)

def addAlbum(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, 'createAlbum.html', context)

def addSong(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, 'createSong.html', context)