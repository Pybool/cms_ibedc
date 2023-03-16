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
load_dotenv()
refresh_jwt_token_life = int(os.getenv("REFRESH_JWT_TOKEN_LIFE"))
ISSUER_NAME = os.getenv("2FA_ISSUER_NAME")

class CustomerCaadView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        permission_hierarchy = generate_slug(request.user.permission_hierarchy)
        user = get_object_or_404(User, email=request.user.email)
        field_name = get_field_name(permission_hierarchy)
        location = permission_hierarchy.replace('-', '_')   
        return Response({})  
    
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
        try:
            if self.field_name is not None:
                queries = { 'region':CaadHeader.objects.filter(**{f"{'region'}__icontains": self.location}),
                            'buid':CaadHeader.objects.filter(region=request.user.region).filter(**{f"{self.field_name}__icontains": self.location}),
                            'servicecenter':CaadHeader.objects.filter(region=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{self.field_name}__icontains": self.location})
                          }
            if id is None:
                locale_positions = ['BHM','OC','RH']
                inverse_last_approvals = {"BHM":"","OC":"BHM APPROVED","RH":"OC APPROVED","HCS":"RH APPROVED","CCO":"HCS APPROVED","MD":"CCO APPROVED"}
                user_position = get_user_position_code(request.user.position)
                if user_position in locale_positions:
                    pending_queue = queries[self.field_name].filter(last_approval = inverse_last_approvals[user_position]).order_by('-created_date').values()
                else:
                    pending_queue = CaadHeader.objects.filter(last_approval = inverse_last_approvals[user_position]).order_by('-created_date').values()
            else:
                line_items = CaadLineItems.objects.filter(header_id = int(id)).values()
                approvers = CaadApprovalUsers.objects.filter(caad_id =int(id)).order_by('-date_approved').values()
                return Response({"status":True,"data":line_items,"approvers":approvers,"message":"Caad Line Items Records where successfully fetched"})
                
            return Response({"status":True,"data":pending_queue,"message":"Caad Records where successfully fetched"})
            
        except Exception as e:
            print(str(e))
            response = {"status":False,"message":f"An error occured while processing your request"} 
            return Response(response)  
    
    def put(self,request):
        if request.user.can_approve_caad:
            self.caad_helper = CaadHelper(request)
            return self.caad_helper.caad_approval()
        else:
            return Response({"status":False,"message":f"Nope, you can not do this!!"})
        
        
        

