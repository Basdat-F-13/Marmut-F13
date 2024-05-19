from django.urls import path
from viewchart.views import *

app_name = 'viewchart'

urlpatterns = [
    path('viewchart', showviewchart, name='viewchart'),
    path('dailypage', showdailypagechart, name='dailypage'),
    path('weeklypage', showweeklypagechart, name='weeklypage'),
    path('monthlypage', showmonthlypagechart, name='monthlypage'),  
    path('yearlypage', showyearlypagechart, name='yearlypage'),
]
