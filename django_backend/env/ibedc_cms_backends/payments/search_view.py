from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import EcmiPaymentHistory
from ibedc_cms_backend.custompagination import CustomPaginatorClass
from config import CACHE_CONTROL
from .raw_queries import *
from authentication.models import User
from django.shortcuts import get_object_or_404
from connection_executor import dict_fetch_all
from helper import generate_slug, get_permission_hierarchy
from rest_framework.pagination import LimitOffsetPagination
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
from location.models import EmsBusinessUnit

def fetch_and_cache_buids():
    data = list(EmsBusinessUnit.objects.filter().values('buid','name','state'))
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
   
class SearchEcmiPayments(APIView):
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
        
        search_type = request.GET.get('type','searchbar')
        
        if search_type == 'datewidget':
            self.past_date = request.GET.get('start_date')
            self.current_date = request.GET.get('end_date')
            self.filter = f" [ecmi_payment_history].transdate BETWEEN CONVERT(DATE,'{self.past_date}') AND CONVERT(DATE,'{self.current_date}')"
            
        
        if search_type == 'searchbar':
            self.field = request.GET.get('field')
            self.value = request.GET.get('value')
            self.filter = f" [ecmi_payment_history].{self.field} = '{self.value}'"
      
        if permission_hierarchy != '' and permission_hierarchy != 'head-quarters':
            if field_name is not None:#For Non-HQ users
                
                if field_name == 'region' or 'state':
                    query =  CUSTOMER_PAYMENTS_ECMI_HIERARCHY_REGION\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",location)\
                        .replace("#DATE_CONJUNCTION#",'AND' + self.filter)
                        
                if field_name == 'buid' or field_name == 'business_unit':
                
                    query =  CUSTOMER_PAYMENTS_ECMI_HIERARCHY_BUSINESS_UNIT\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",request.user.region)\
                        .replace("#BUID#",location)\
                        .replace("#DATE_CONJUNCTION#",'AND' + self.filter)
                    
                if field_name == 'servicecenter':
                    query =  CUSTOMER_PAYMENTS_ECMI_HIERARCHY_SERVICE_CENTER\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",request.user.region)\
                        .replace("#BUID#",request.user.business_unit)\
                        .replace("#SERVICECENTER#",location)\
                        .replace("#DATE_CONJUNCTION#",'AND' + self.filter)
                    
        else:
            query =  CUSTOMER_PAYMENTS_ECMI_NO_HIERARCHY\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#DATE_CONJUNCTION#",'WHERE' + self.filter)
                    
        self.custom_paginator = CustomPaginatorClass(SearchEcmiPayments.pagination_class,request)
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
          
class SearchEmsPayments(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def get(self, request):
       
        page_no = '1'#str(request.GET.get('page', 2))
        page_size = str(request.GET.get('page_size', 250))
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        query = None
     
        search_type = request.GET.get('type','searchbar')
        print(search_type)
        
        if search_type == 'datewidget':
            self.past_date = request.GET.get('start_date')
            self.current_date = request.GET.get('end_date')
            self.filter = f" [ems_payments].PayDate BETWEEN CONVERT(DATE,'{self.past_date}') AND CONVERT(DATE,'{self.current_date}')"
        
        if search_type == 'searchbar':
            self.field = request.GET.get('field')
            self.value = request.GET.get('value')
            self.filter = f" [ems_payments].{self.field} = '{self.value}'"
            
        if permission_hierarchy != '' and permission_hierarchy != 'head-quarters':
            if field_name is not None:#For Non-HQ users
                
                if field_name == 'region' or 'state':
                    query =  CUSTOMER_PAYMENTS_EMS_HIERARCHY_REGION\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",location)\
                        .replace("#DATE_CONJUNCTION#",'AND' + self.filter)
                        
                if field_name == 'buid':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(location, request.user.region, buids)
                    query =  CUSTOMER_PAYMENTS_EMS_HIERARCHY_BUSINESS_UNIT\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",request.user.region)\
                        .replace("#BUID#",buid)\
                        .replace("#DATE_CONJUNCTION#",'AND' + self.filter)
                    
                if field_name == 'servicecenter':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(request.user.business_unit, '', buids,alt='name')
                    query =  CUSTOMER_PAYMENTS_EMS_HIERARCHY_SERVICE_CENTER\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#REGION#",request.user.region)\
                        .replace("#BUID#",buid)\
                        .replace("#SERVICECENTER#",location)\
                        .replace("#DATE_CONJUNCTION#",'AND' + self.filter)
                    
        else:
            query =  CUSTOMER_PAYMENTS_EMS_NO_HIERARCHY\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#DATE_CONJUNCTION#",'WHERE' + self.filter)
                        
        self.custom_paginator = CustomPaginatorClass(SearchEmsPayments.pagination_class,request)
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
