from django.urls import include, path
from .views import *

urlpatterns = [
   path('singlecustomer-payments', SingleCustomerPayments.as_view()),
      
]