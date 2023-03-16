from django.urls import include, path
from .views import *
from .draftviews import *

urlpatterns = [
   path('cms/drafts', DraftsView.as_view()),
   path('cms/awaiting_customer', CustomerEditQueueView.as_view())

]