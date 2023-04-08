from django.urls import include, path
from .views import *

urlpatterns = [
   path('cms/admin/locations', LocationView.as_view()),
    path('locations/getdata', PermissionsHierarchyView.as_view()),
   
]

