# (select max(create_date) from res_users_log where res_users.id = res_users_log.create_uid) as last_authentication,

import uuid
from authentication.helpers.permissions import Permissions
from config import CACHE_CONTROL, PAGINATION_SETTINGS
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
# import stripe
from authentication.cms_authenticate import  JWTAuthenticationMiddleWare
from dotenv import load_dotenv

from django.db import transaction
from decorators import is_caad_initiator, is_valid_caad_bha
from tasks.__task__email import send_outward_mail
from tasks.models import UserTasksInbox
load_dotenv()


class UserTasks(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        task_type = request.GET.get('task_type') or 'CAAD'
        status = request.GET.get('status')
        if status is None:
            tasks = UserTasksInbox.objects.filter(user__id=request.user.id,task_type=task_type).values() 
        else:
            status = True if status == '1' else False
            tasks = UserTasksInbox.objects.filter(user__id=request.user.id,task_type=task_type,status=status).values() 
        if tasks:
            return Response({"status":True,"message":f"Tasks for {task_type} were successfully retrieved","tasks":tasks})  
        return Response({"status":False,"message":f"Tasks for {task_type} could not be retrieved at this time"})
    
    