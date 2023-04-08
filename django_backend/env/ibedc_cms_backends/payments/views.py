import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
# from ibedc_cms_backend.configurations import CACHE_CONTROL, PAGINATION_SETTINGS
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from authentication.models import User
from django.utils.text import slugify
import itertools
from config import CACHE_CONTROL
from rest_framework.pagination import LimitOffsetPagination
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
from connection_executor import dict_fetch_all
from .raw_queries import *
from .models import EcmiPaymentHistory,EcmiTransactions
from helper import generate_slug, get_permission_hierarchy
from ibedc_cms_backend.custompagination import CustomPaginatorClass
from location.models import EmsBusinessUnit


def fetch_and_cache_buids():
    # data = cache.get('buids')
    # if not data:
    data = list(EmsBusinessUnit.objects.filter().values('buid','name','state'))
        # cache.set('buids', data)
    return data

def search_for_buid(name,state,lst,alt=None):
    for d in lst:
        if alt is None:
            if d["name"].lower() == name.lower() and d["state"].lower() == state.lower():
                return d["buid"]
        else:
            if d["name"].lower() == name.lower():
                return d["buid"]
    return None

class SingleCustomerPayments(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        accountno = request.GET.get('accountno')
        accounttype = request.GET.get('accounttype')
        page_no = str(request.GET.get('page', 1))
        page_size = str(request.GET.get('page_size', 10))
        if accounttype == 'postpaid':
            query =  SINGLE_CUSTOMER_PAYMENTS_EMS\
                        .replace("#AccountNo#",accountno)\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)
        else:
            query =  SINGLE_CUSTOMER_PAYMENTS_ECMI\
                        .replace("#AccountNo#",accountno)\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)
        print(query)
      
        payments = dict_fetch_all(query)#Emspayments.objects.filter(accountno__iexact=accountno).all().order_by('id')[:10]
        if payments:
            response = {"status": True, "count":0, "data": payments}
        else:
            response = {"status": False, "message": "No customer payments found "}
        return Response(response)

class CustomerEcmiPayments(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def get(self, request):
       
        page_no = str(request.GET.get('page', 1))
        page_size = str(request.GET.get('page_size', 100))
        
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        use_raw = True
        query = None
      
        print(permission_hierarchy, permission_hierarchy)
        if permission_hierarchy != '' and permission_hierarchy != 'head-quarters':
            if field_name is not None:#For Non-HQ users
                
                if field_name == 'region' or 'state':
                    query =  CUSTOMER_PAYMENTS_ECMI_HIERARCHY_REGION\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",location)\
                        .replace("#DATE_CONJUNCTION#",'')
                        
                if field_name == 'buid' or field_name == 'business_unit':
                   
                    query =  CUSTOMER_PAYMENTS_ECMI_HIERARCHY_BUSINESS_UNIT\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",request.user.region)\
                        .replace("#BUID#",location)\
                        .replace("#DATE_CONJUNCTION#",'')
                    
                if field_name == 'servicecenter':
                    query =  CUSTOMER_PAYMENTS_ECMI_HIERARCHY_SERVICE_CENTER\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",request.user.region)\
                        .replace("#BUID#",request.user.business_unit)\
                        .replace("#SERVICECENTER#",location)\
                        .replace("#DATE_CONJUNCTION#",'')
                    
        else:
            query =  CUSTOMER_PAYMENTS_ECMI_NO_HIERARCHY\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#DATE_CONJUNCTION#",'')
                        
        self.custom_paginator = CustomPaginatorClass(CustomerEcmiPayments.pagination_class,request)
        payments = None
        total_payments = 0#bills_query.count()
        print(query)
        payments = dict_fetch_all(query)
        
        if payments:
            payments = self.custom_paginator.paginate_queryset(payments)
            response = self.custom_paginator.get_paginated_response(payments)
            response.data["status"] = True
            response.data["message"] = "ECMI payments were successfully fetched"
            response.data["data"] = response.data.pop('results')
            response.data["total_payments"] = total_payments
            response.data["rawQueryUsed"] = query is not None
            
        else:
            response = Response({"status": False, "message": "No customer payments found "})
        response_cc = response
        response_cc.headers['Cache-Control'] = CACHE_CONTROL
        return response_cc
          
class CustomerEmsPayments(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def get(self, request):
       
        page_no = '1'#str(request.GET.get('page', 2))
        page_size = str(request.GET.get('page_size', 250))
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        query = None
     
        print(permission_hierarchy, permission_hierarchy)
        if permission_hierarchy != '' and permission_hierarchy != 'head-quarters':
            if field_name is not None:#For Non-HQ users
                
                if field_name == 'region' or 'state':
                    query =  CUSTOMER_PAYMENTS_EMS_HIERARCHY_REGION\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",location)\
                        .replace("#DATE_CONJUNCTION#",'')
                        
                if field_name == 'buid':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(location, request.user.region, buids)
                    query =  CUSTOMER_PAYMENTS_EMS_HIERARCHY_BUSINESS_UNIT\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",request.user.region)\
                        .replace("#BUID#",buid)\
                        .replace("#DATE_CONJUNCTION#",'')
                    
                if field_name == 'servicecenter':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(request.user.business_unit, '', buids,alt='name')
                    query =  CUSTOMER_PAYMENTS_EMS_HIERARCHY_SERVICE_CENTER\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",request.user.region)\
                        .replace("#BUID#",buid)\
                        .replace("#SERVICECENTER#",location)\
                        .replace("#DATE_CONJUNCTION#",'')
                    
        else:
            query =  CUSTOMER_PAYMENTS_EMS_NO_HIERARCHY\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#DATE_CONJUNCTION#",'')
                        
        self.custom_paginator = CustomPaginatorClass(CustomerEcmiPayments.pagination_class,request)
        payments = None
        total_payments = 0#bills_query.count()
        print(query)
        payments = dict_fetch_all(query)
        
        if payments:
            payments = self.custom_paginator.paginate_queryset(payments)
            response = self.custom_paginator.get_paginated_response(payments)
            response.data["status"] = True
            response.data["message"] = "EMS payments were successfully fetched"
            response.data["data"] = response.data.pop('results')
            response.data["total_payments"] = total_payments
            response.data["rawQueryUsed"] = query is not None
            
        else:
            response = Response({"status": False, "message": "No customer payments found "})
        response_cc = response
        response_cc.headers['Cache-Control'] = CACHE_CONTROL
        return response_cc

class Initializer(object):
    
    def __init__(self,request):
        
        self.user = request.user
        self.permissions_dict = {}
        self.hierarchy_order = {}
        
    def get_hierarchy(self)->dict:
        self.key = None
        self.hierarchy_order = {
            'state': self.user.is_level_user('Region'),
            'buid': self.user.is_level_user('Business Unit'),
            'servicecenter': self.user.is_level_user('Service Center'),
            'hq': self.user.is_level_user('Head Quarters'),
        }
        for key, val in self.hierarchy_order.items():
            if val:
                self.key = key
                break
            
        self.permissions_dict = {
            'state': self.user.region,
            'buid': self.user.business_unit,
            'servicecenter': self.user.service_center,
            'bucode': self.user.bucode
        }
        return {"key":self.key,"permissions_dict":self.permissions_dict,'hierarchy_order':self.hierarchy_order}
    
class TodayCollectionsEcmi(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    
    def get(self,request):
        from dashboard.helpers.todays_collection import Collections
        self.current_date = '2022-02-28'
        self.past_date = '2022-02-28'
        self.initializer = Initializer(request)
        obj = self.initializer.get_hierarchy()
        self.collections = Collections(1,self.past_date,self.current_date,obj.get('key'),obj.get('permissions_dict'),obj.get('hierarchy_order'),request)
        query = self.collections.todays_collections('ecmi')
        print("Today collections ------> ",query)
        self.custom_paginator = CustomPaginatorClass(TodayCollectionsEcmi.pagination_class,request)
        payments = None
        total_payments = 0#bills_query.count()
        print(query)
        payments = dict_fetch_all(query)
        
        if payments:
            payments = self.custom_paginator.paginate_queryset(payments)
            response = self.custom_paginator.get_paginated_response(payments)
            response.data["status"] = True
            response.data["message"] = "ECMI payments were successfully fetched"
            response.data["data"] = response.data.pop('results')
            response.data["total_payments"] = total_payments
            response.data["rawQueryUsed"] = query is not None
            
        else:
            response = Response({"status": False, "message": "No customer payments found "})
        response_cc = response
        response_cc.headers['Cache-Control'] = CACHE_CONTROL
        return response_cc
    
class TodayCollectionsEms(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    
    def get(self,request):
        from dashboard.helpers.todays_collection import Collections
        self.current_date = '2022-02-28'
        self.past_date = '2022-02-28'
        self.initializer = Initializer(request)
        obj = self.initializer.get_hierarchy()
        self.collections = Collections(1,self.past_date,self.current_date,obj.get('key'),obj.get('permissions_dict'),obj.get('hierarchy_order'),request)
        query = self.collections.todays_collections('ems')
        print("Today collections EMS------> ",query)
        self.custom_paginator = CustomPaginatorClass(TodayCollectionsEms.pagination_class,request)
        payments = None
        total_payments = 0#bills_query.count()
        print(query)
        payments = dict_fetch_all(query)
        
        if payments:
            payments = self.custom_paginator.paginate_queryset(payments)
            response = self.custom_paginator.get_paginated_response(payments)
            response.data["status"] = True
            response.data["message"] = "EMS payments were successfully fetched"
            response.data["data"] = response.data.pop('results')
            response.data["total_payments"] = total_payments
            response.data["rawQueryUsed"] = query is not None
            
        else:
            response = Response({"status": False, "message": "No customer payments found "})
        response_cc = response
        response_cc.headers['Cache-Control'] = CACHE_CONTROL
        return response_cc