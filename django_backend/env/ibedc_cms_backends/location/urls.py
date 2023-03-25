from django.urls import include, path
from .views import *

urlpatterns = [
   path('locations/getdata', PermissionsHierarchyView.as_view()),
   
]

