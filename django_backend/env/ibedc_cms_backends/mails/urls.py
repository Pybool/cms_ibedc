from django.urls import include, path
from .views import *

urlpatterns = [
   path('mailtest', Test.as_view()),
       
]