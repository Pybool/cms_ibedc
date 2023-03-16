from django.urls import include, path
from .views import *

urlpatterns = [
   path('singlecustomer-bills', SingleCustomerBills.as_view()),
   path('customers-bills', CustomerBills.as_view()),
      
]