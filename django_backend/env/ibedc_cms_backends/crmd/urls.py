from django.urls import include, path
from .views import *

urlpatterns = [
   path('cms/customerform/metadata', CustomerFormMetaDataView.as_view()),
   path('cms/awaiting/customers', AwaitingCustomersView.as_view()),
   
   
]