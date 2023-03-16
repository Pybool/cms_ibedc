from django.urls import include, path
from .views import *

urlpatterns = [
   path('customers/prepaid', PrepaidCustomers.as_view()),
   path('customers/postpaid', PostpaidCustomers.as_view()),
   path('customer/information/basic-information', SingleCustomer.as_view()),  
#    /
   
]