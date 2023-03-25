from django.urls import include, path
# from rest_framework import routers
from .views import *

urlpatterns = [
   path('dashboard/account_types/feeders/recentpayments', AccountTypesView.as_view()),
   path('dashboard/opsmanager/collections_statistics',OpsmanagerView.as_view()),
   path('dashboard/todayscols/meteringstatistics',TodayCollectionsView.as_view()),
   
   
   
   
]