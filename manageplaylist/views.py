from django.shortcuts import render

# Create your views here.
def showManagePlaylistPage(request):
    return render(request, "manageplaylist.html", {})

def showPlaylistPage(request):
    return render(request,"userplaylistdetail.html",{} )

def showPlayingSongPage(request):
    return render(request,"playsong.html",{} )