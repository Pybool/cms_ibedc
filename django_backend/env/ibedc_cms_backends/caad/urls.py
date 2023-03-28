from django.urls import include, path
from .views import *

urlpatterns = [
   path('cms/customer/caad', CustomerCaadView.as_view()),
   path('cms/caadlist',CaadApprovalsView.as_view()),
   path('cms/customer/initiate-caad',GetInitiateOrDeclineCAADTask.as_view())
   ]