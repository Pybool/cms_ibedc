import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
# from ibedc_cms_backend.configurations import CACHE_CONTROL, PAGINATION_SETTINGS
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .models import EmsBills
from authentication.models import User
from django.utils.text import slugify
import itertools
from rest_framework.pagination import LimitOffsetPagination
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
from connection_executor import dict_fetch_all
from .raw_queries import *
from helper import generate_slug, get_field_name
from ibedc_cms_backend.custompagination import CustomPaginatorClass
from helper import generate_slug, get_permission_hierarchy
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


class SingleCustomerBills(APIView):
    # authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        accountno = request.GET.get('accountno')
        page_no = str(request.GET.get('page', 1))
        page_size = str(request.GET.get('page_size', 10))
        query =  SINGLE_CUSTOMER_BILLS\
                    .replace("#AccountNo#",accountno)\
                    .replace("#page_size#",page_size)\
                    .replace("#page_no#",page_no)
        bills = dict_fetch_all(query)#EmsBills.objects.filter(accountno__iexact=accountno).all().order_by('id')[:10]
        if bills:
            response = {"status": True, "count":0, "data": bills}
        else:
            response = {"status": False, "message": "No customer bills found with the provided account number."}
        return Response(response)


class CustomerBills(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def get(self, request):
        accountno = request.GET.get('accountno')
        page_no = '42'#str(request.GET.get('page', 2))
        page_size = str(request.GET.get('page_size', 250))
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        use_raw = True
        query = None
        if permission_hierarchy != generate_slug(user.permission_hierarchy):
            response = {"status":False, "message":"Hierarchy specified does not match legacy", "data":[]}
            return Response(response)
        
        print(permission_hierarchy, permission_hierarchy)
        if permission_hierarchy != '' and permission_hierarchy != 'head-quarters':
            if field_name is not None:#For Non-HQ users
                
                if field_name == 'region':
                    query =  BILLING_HISTORY_HIERARCHY_REGION\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#hierarchy#",field_name)\
                        .replace("#hierarchy_value#",location)
                        
                elif field_name == 'buid':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(location, request.user.region, buids)
                    query =  BILLING_HISTORY_HIERARCHY_BUID\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#hierarchy#",field_name)\
                        .replace("#hierarchy_value#",request.user.region)\
                        .replace("#BUID#",buid)\
                    
                elif field_name == 'servicecenter':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(request.user.business_unit, '', buids,alt='name')
                    query =  BILLING_HISTORY_HIERARCHY_SERVICECENTER\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#hierarchy#",field_name)\
                        .replace("#hierarchy_value#",request.user.region)\
                        .replace("#BUID#",buid)\
                        .replace("#SERVICECENTER#",location)
                    
        else:
            query =  BILLING_HISTORY_NO_HIERARCHY\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)
        self.custom_paginator = CustomPaginatorClass(CustomerBills.pagination_class,request)
        bills = None
        bills_query = EmsBills.objects.all().order_by('-billdate')[:10000]
        total_bills = 0#bills_query.count()
        bills = bills_query.values() if use_raw is False else print(45000)#dict_fetch_all(query)
        bills = dict_fetch_all(query)
        print(query)
        if bills:
            bills = self.custom_paginator.paginate_queryset(bills)
            response = self.custom_paginator.get_paginated_response(bills)
            response.data["status"] = True
            response.data["message"] = "EMS bills were successfully fetched"
            response.data["data"] = response.data.pop('results')
            response.data["total_bills"] = total_bills
            response.data["rawQueryUsed"] = query is not None
            
        else:
            response = {"status": False, "message": "No customer bills found with the provided account number."}
        return response
        