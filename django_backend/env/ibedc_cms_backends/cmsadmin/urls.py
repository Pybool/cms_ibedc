
from django.urls import include, path
# from rest_framework import routers
from ._locations_views import *

urlpatterns = [
   path('cms/permissions/get_hierarchy_data/',get_hierarchy_data, name = 'get_hierarchy_data'),
]

