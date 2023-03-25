from django.urls import include, path
from .views import *
from .search_view import *

urlpatterns = [
   path('singlecustomer-bills', SingleCustomerBills.as_view()),
   path('customers-bills', CustomerBills.as_view()),
   path('search-customers-bills', SearchCustomerBills.as_view()),
      
]