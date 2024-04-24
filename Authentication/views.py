from django.shortcuts import render

# Create your views here.
def showLoginPage(request):
    return render(request, "loginPage.html", {})