from django.urls import include, path
from .views import *

urlpatterns = [
   path('singlecustomer-meteringInfo', SingleCustomerMetering.as_view()),
      
]