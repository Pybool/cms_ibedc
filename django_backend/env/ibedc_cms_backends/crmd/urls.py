from django.urls import include, path
from .views import *

urlpatterns = [
   path('cms/customerform/metadata', CustomerFormMetaDataView.as_view()),
   path('cms/awaiting/customers', AwaitingCustomersView.as_view()),
   path('cms/get_edits_status', PendingCustomerEditsView.as_view()),
]