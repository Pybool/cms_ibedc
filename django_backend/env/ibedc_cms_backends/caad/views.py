# (select max(create_date) from res_users_log where res_users.id = res_users_log.create_uid) as last_authentication,

import logging
import uuid
from authentication.helpers.permissions import Permissions
from config import CACHE_CONTROL, PAGINATION_SETTINGS
log = logging.getLogger(__name__)
from collections import namedtuple
import os, datetime as dt
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
# import stripe
from authentication.models import AuthGroup, ResetPassword, User, UserJWTtokens, UserPositions
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare, create_access_token, 
                                              create_refresh_token, decode_access_token, decode_refresh_token
                                            )
from dotenv import load_dotenv
from .viewshelper import CaadHelper
from django.db import transaction
from helper import generate_slug, get_field_name, get_permission_hierarchy,get_user_position_code
from .models import CaadHeader, CaadLineItems, CaadApprovalUsers
from decorators import is_caad_initiator, is_valid_caad_bha
from tasks.__task__email import send_outward_mail
from tasks.models import UserTasksInbox
load_dotenv()
refresh_jwt_token_life = int(os.getenv("REFRESH_JWT_TOKEN_LIFE"))
ISSUER_NAME = os.getenv("2FA_ISSUER_NAME")

class CustomerCaadView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        permission_hierarchy = generate_slug(request.user.permission_hierarchy)
        user = get_object_or_404(User, email=request.user.email)
        customer_caads = CaadHeader.objects.filter(account_no = request.GET.get('account_no')).values()
        response =  Response({"status":True, "data":customer_caads,"message":"Customer CAAD recors were successfully fetched"}) 
        response.headers['cache']  = CACHE_CONTROL
        return response
    
    def post(self,request):
        self.caad_helper = CaadHelper(request)
        return self.caad_helper.create_refund_view()
    
    def put(self,request):
        self.caad_helper = CaadHelper(request)
        return self.caad_helper.create_refund_view()
    
    

class CaadApprovalsView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        id = request.GET.get('id',None)    
        self.field_name, self.location = get_permission_hierarchy(request)
        print(self.field_name, self.location)
        # try:
        if self.field_name is not None:
            queries = { 'region':CaadHeader.objects.filter(**{f"{'region'}__icontains": self.location}),'state':CaadHeader.objects.filter(**{f"{'region'}__icontains": self.location}),
                        'buid':CaadHeader.objects.filter(region=request.user.region).filter(**{f"{self.field_name}__icontains": self.location}),
                        'servicecenter':CaadHeader.objects.filter(region=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{self.field_name}__icontains": self.location})
                        }
        if id is None:
            locale_positions = ['BHA','BHM','OC','RH']
            inverse_last_approvals = {"BHA":"","BHM":"BHA APPROVED","OC":"BHM APPROVED","RH":"OC APPROVED","HCS":"RH APPROVED","CCO":"HCS APPROVED","MD":"CCO APPROVED"}
            user_position = get_user_position_code(request.user.position)
            if user_position in locale_positions:
                pending_queue = queries[self.field_name].filter(last_approval = inverse_last_approvals[user_position],revert_status=False).order_by('-created_date').values()
            else:
                pending_queue = CaadHeader.objects.filter(last_approval = inverse_last_approvals[user_position],revert_status=False).order_by('-created_date').values()
        else:
            line_items = CaadLineItems.objects.filter(header_id = int(id)).values()
            approvers = CaadApprovalUsers.objects.filter(caad_id =int(id)).order_by('-date_approved').values()
            return Response({"status":True,"data":line_items,"approvers":approvers,"message":"Caad Line Items Records where successfully fetched"})
            
        return Response({"status":True,"data":pending_queue,"message":"Caad Records where successfully fetched"})
            
        # except Exception as e:
        #     print(str(e))
        #     response = {"status":False,"message":f"An error occured while processing your request"} 
        #     return Response(response)  
    
    def put(self,request):
        if request.user.can_approve_caad:
            self.caad_helper = CaadHelper(request)
            return self.caad_helper.caad_approval()
        else:
            return Response({"status":False,"message":f"Nope, you can not do this!!"})

class GetInitiateOrDeclineCAADTask(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    @is_caad_initiator()
    def post(self,request):
        data = request.data
        firstname = data.get('firstname') or ''
        surname = data.get('surname') or ''
        othernames = data.get('othernames') or ''
        full_name = ' '.join([firstname, surname, othernames]).strip()
        servicecenter = data.get('servicecenter')
        print(servicecenter,data.get('buid'))
        rpus_list = User.objects.filter(service_center__icontains=servicecenter).filter(position__icontains='RPU').values('email')
        rpus = []
        try:
            print("The rpus ", rpus_list)
            if len(rpus_list) < 1:
                rpus_list = User.objects.filter(business_unit__icontains=data.get('buid')).filter(position__icontains='RPU').values('email')
                print("=====-----***&&&....> ", rpus_list)
        except:
            rpus_list = []
        for rpu in rpus_list:
            rpus.append(rpu.get('email'))
        mail_parameters = {"ir_template":"caad_initiate",
            "url":"",
            "subject":"Customer Account Adjustment Document Initiated",
            "sender":request.user.email, 
            "body":data,
            "recipients":rpus}
        print("Mail parameter ====> ", mail_parameters)
        if len(rpus) > 0:
            task = {"user":get_object_or_404(User,email=rpus[0]),"taskid":uuid.uuid4(),
                    "task_description":f"Conduct second level validation for CAAD at the premises of {full_name} at address {data.get('address',data.get('address1'))}",
                    "task_sentby":request.user.email,"created_by":request.user.email,"associated_customer":data.get('accountno')}
            status = UserTasksInbox.objects.create(**task)
            print(status)
            send_outward_mail.delay(mail_parameters)

            task['task_owner_name'] = task['user'].name
            task['task_owner_mail'] = task['user'].email
            task.pop('user')
            return Response({"status":True,"message":"A mail has been sent to the Revenue Protection Unit at the service center for this customer","task":task})
        else:
            return Response({"status":False,"message":"Could not perform this action at this time, there is no recipient for this action"})
        
    @is_valid_caad_bha()
    def put(self,request):
        task_id = request.data.get('task_id')
        status = request.data.get('status')
        status = True if status == '1' else False
        UserTasksInbox.objects.filter(taskid=task_id).update(status=status)
        return Response({"status":True,"message":"This CAAD submission by RPU has been updated"})
        