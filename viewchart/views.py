from django.shortcuts import render

# Create your views here.
def showviewchart(request):
    return render(request, "viewchart.html", {})

def showdailypagechart(request):
    return render(request, "dailypage.html", {})

def showweeklypagechart(request):
    return render(request, "weeklypage.html", {})

def showdmonthlypagechart(request):
    return render(request, "monthlypage.html", {})

def showyearlypagechart(request):
    return render(request, "yearlypage.html", {})