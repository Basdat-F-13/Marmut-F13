from django.shortcuts import render

# Create your views here.
def showmanagepod(request):
    return render(request, "managepod.html", {})

def showlist(request):
    return render(request, "list.html", {})

def showcreatepod(request):
    return render(request, "createpod.html", {})

def showaddepisode(request):
    return render(request, "addepisode.html", {})