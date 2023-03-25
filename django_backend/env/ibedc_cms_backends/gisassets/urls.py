from django.urls import include, path
from .views import *

urlpatterns = [
   path('singlecustomer-assets', SingleCustomerAssets.as_view()),
   path('cms/gis/getasset_info', FetchGisAssetInfo.as_view()),
   path('cms/gis/getfeeder_info', FetchFeederView.as_view()),
   
   
      
]