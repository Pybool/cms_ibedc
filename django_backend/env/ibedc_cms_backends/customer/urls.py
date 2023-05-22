from django.urls import include, path
from .views import *
from .search_view import *

urlpatterns = [
   path('customers/prepaid', PrepaidCustomers.as_view()),
   path('customers/postpaid', PostpaidCustomers.as_view()),
   path('customer/information/basic-information', SingleCustomer.as_view()), 
   path('searching/prepaid/customers', SearchPrepaidCustomers.as_view()),
   path('advancedsearching/prepaid/customers', AdvancedSearchPrepaidCustomers.as_view()),
   path('searching/postpaid/customers', SearchPostpaidCustomers.as_view()),
   path('advancedsearching/postpaid/customers', AdvancedSearchPostpaidCustomers.as_view()),
   path('singlecustomer/tariffcode', TarrifCode.as_view()),
   
   
     
   

]