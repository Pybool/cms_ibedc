from django.urls import include, path
from .views import *
from .search_view import *

urlpatterns = [
   path('singlecustomer-payments', SingleCustomerPayments.as_view()),
   path('customers-ecmi-payments', CustomerEcmiPayments.as_view()),
   path('customers-ems-payments', CustomerEmsPayments.as_view()),
   path('todaycollections-ecmi', TodayCollectionsEcmi.as_view()),
   path('todaycollections-ems', TodayCollectionsEms.as_view()),
   
   path('search-customers-ecmi-payments', SearchEcmiPayments.as_view()),
   path('search-customers-ems-payments', SearchEmsPayments.as_view()),   
]