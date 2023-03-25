from django.urls import include, path
from .views import *

urlpatterns = [
   path('cms/settings/create_options', CreateOptions.as_view()),
   path('cms/settings/read_options/', ReadSettingsView.as_view()),
   path('cms/settings/options/', Options.as_view()),
    path('cms/settings/update_options', UpdateSettingsView.as_view()),
    path('cms/settings/delete_options', DeleteSettingsView.as_view()),
    path('cms/settings/getdata', SettingsView.as_view()),
    path('cms/settings/update_role_hierarchy/', UpdateHierarchyView.as_view()),
        
    
    
   
   
  
]