# (select max(create_date) from res_users_log where res_users.id = res_users_log.create_uid) as last_authentication,

import logging
import uuid
from authentication.helpers.permissions import Permissions
from config import CACHE_CONTROL, PAGINATION_SETTINGS
from usergroups.views import GroupUtils
from cmsadmin.models import LocationsPermissions
log = logging.getLogger(__name__)
from collections import namedtuple
import os, datetime as dt
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import generics
from django.db.models import Q
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
# import stripe
from rest_framework.permissions import IsAuthenticated
from authentication.models import AuthGroup, ResetPassword, User, UserJWTtokens, UserPositions
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare, create_access_token, 
                                 create_refresh_token, decode_access_token, decode_refresh_token
                                 )
from dotenv import load_dotenv
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from usergroups.models import AuthenticationUserGroups
from helper import generate_slug, get_field_name, get_permission_hierarchy,get_user_position_code
from location.views import PermissionsHierarchyView
from accountsmanager.models import CustomerEditQueue
from crmd.approvals import Approvals
from configurations.models import UserProcessHierarchy, AccountType,BuildingDescription, CustomerCategory,CustomerType,PremiseType,SupplyType,ServiceBand, CaadVat

load_dotenv()
refresh_jwt_token_life = int(os.getenv("REFRESH_JWT_TOKEN_LIFE"))
ISSUER_NAME = os.getenv("2FA_ISSUER_NAME")

model_map = {
                'accounttype': AccountType,
                'building_description': BuildingDescription,
                'customer_category': CustomerCategory,
                'customer_type': CustomerType,
                'premise_type': PremiseType,
                'supply_type': SupplyType,
                'service_band': ServiceBand,
            }

def get_options():
    options_object_dict = {}
    for model_key in model_map.keys():
        options_object =  model_map[model_key].objects.filter().values('name', 'code')
        options_object_dict[model_key] = options_object
    
    return options_object_dict

class CustomerFormMetaDataView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        permission_hierarchy = generate_slug(request.user.permission_hierarchy)
        user = get_object_or_404(User, email=request.user.email)
        field_name = get_field_name(permission_hierarchy)
        location = permission_hierarchy.replace('-', '_')        
        # print("Location ====> ", field_name, getattr(user, location))
        
        if field_name == 'state':
            locations = PermissionsHierarchyView.get(PermissionsHierarchyView,request,{'as_method':True,'hierarchy':'business_unit','q':location})
            locations['type'] = 'business_units'
                    
        elif field_name == 'business_unit':
            locations = PermissionsHierarchyView.get(PermissionsHierarchyView,request,{'as_method':True,'hierarchy':'servicecenter','q':location})
            locations['type'] = 'service_centers'
            
        else:
            locations = []
            
        options_object_dict = get_options()
        
        if permission_hierarchy == generate_slug(user.permission_hierarchy):
            return Response({'status':True,'locations':locations,'options_object_dict':options_object_dict})


class AwaitingCustomersView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        if request.user.can_approve:
            awaiting_customers = []
            status = request.GET.get('status','pending')
            field_name, location = get_permission_hierarchy(request)
            position_code = get_user_position_code(request.user.position)
            queries = {'region':CustomerEditQueue.objects.filter(**{f"{field_name}__icontains": location}),
                        'buid':CustomerEditQueue.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": location}),
                        'servicecenter':CustomerEditQueue.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location})}
            if position_code == 'BHM':
                awaiting_customers = queries[field_name].filter(status=status.title()).filter(bhm_aproved=False,auditor_approved=False).values()
                
            elif position_code == 'ADT':
                awaiting_customers = queries[field_name].filter(status=status.title()).filter(bhm_aproved=True,auditor_approved=False).values()
            if awaiting_customers:
                return Response({"status":True, 'data':awaiting_customers,'message':f'{status.title()} customers were fetched successfully'})
            return Response({"status":False, 'data':list(),'message':f'{status.title()} customers could not be fetched at this time'})
        else:
            return Response({"status":False,'code':8005, 'data':list(),'message':f'Unauthorized access'})
    def put(self,request):
        data = request.data
        print(data)
        data['approved_by'] = request.user.email
        self.is_fresh = data.get('is_fresh',False)
        self.user_position_code = get_user_position_code(request.user.position)
        self.field_name, self.location = get_permission_hierarchy(request)
        if self.user_position_code == 'ADT': # If the Auditor is approving then final status can be set to Approved, else leave as Pending
            data['status'] = 'Approved' if data['action'] == 'approve' else 'Declined'
        else:
            data['status'] = 'Pending'
        
        args = {'position_code':self.user_position_code,'field_name':self.field_name,'location':self.location}
        self.approvals = Approvals(args)
        if not self.is_fresh:
            return self.approvals.treat_as_unfresh(data)
        
        elif self.is_fresh:
            return self.approvals.treat_as_fresh(data)

        # if awaiting_customers:
        #     return Response({"status":True, 'data':awaiting_customers,'message':f'{status.title()} customers were fetched successfully'})
        # return Response({"status":False, 'data':list(),'message':f'{status.title()} customers could not be fetched at this time'})