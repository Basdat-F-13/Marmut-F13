from django.shortcuts import render

# Create your views here.
def showplaypodcast(request):
    return render(request, "playpodcast.html", {})