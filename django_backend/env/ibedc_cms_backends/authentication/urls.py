from django.urls import include, path
from .views import *

urlpatterns = [
   path('signup', AuthSignup.as_view()),
   path('login', AuthSignin.as_view()),
   path('userform/metadata', UserFormView.as_view()),
   path('userfactory', CreateUpdateUser.as_view()),
   path('admin/users', GetUsersView.as_view()),
   path('admin/usergroups', GetUserGroupsView.as_view()),
   
   
   
   
]