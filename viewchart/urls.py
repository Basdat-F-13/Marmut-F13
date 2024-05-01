from django.urls import path
from viewchart.views import *

app_name = 'viewchart'

urlpatterns = [
    path('viewchart', showviewchart, name='viewchart'),
    path('dailypage', showdailypagechart, name='dailypage'),  # Add this line
    path('weeklypage', showweeklypagechart, name='weeklypage'),  # Add this line
    path('monthlypage', showdmonthlypagechart, name='monthlypage'),  # Add this line
    path('yearlypage', showyearlypagechart, name='yearlypage'),  # Add this line
]
