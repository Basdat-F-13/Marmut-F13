from django.shortcuts import render

# Create your views here.
def showLoginPage(request):
    context = {
        'show_navbar' : False
    }
    return render(request, "loginPage.html", context)

def showAuthNav(request):
    context = {
        'show_navbar' : False,
    }
    return render(request, "authNav.html", context)

def showNav(request):
    context = {
        'show_navbar' : True,
        'premium' : False,
        'user' : True,
        'artist' : False,
        'songwriter' : False,
        'podcast' : True,
        'label' : False
    }
    return render(request, "base.html", context)
