from django.urls import include, path
from .views import *

urlpatterns = [
   path('singlecustomer-payments', SingleCustomerPayments.as_view()),
   path('customers-ecmi-payments', CustomerEcmiPayments.as_view()),
   path('customers-ems-payments', CustomerEmsPayments.as_view()),
   path('todaycollections-ecmi', TodayCollectionsEcmi.as_view()),
   path('todaycollections-ems', TodayCollectionsEms.as_view()),
       
]