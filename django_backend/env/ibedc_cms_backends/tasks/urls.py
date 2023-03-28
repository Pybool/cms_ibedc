from django.urls import include, path
from .views import *

urlpatterns = [
   path('cms/user/tasks', UserTasks.as_view()),
   ]