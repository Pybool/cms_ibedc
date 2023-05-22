import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
# from ibedc_cms_backend.configurations import CACHE_CONTROL, PAGINATION_SETTINGS
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .fields import ECMI_FIELDS, EMS_FIELDS
from .models import EcmiCustomersNew, EmsCustomersNew, EcmiTariff, EmsTariff
from authentication.models import User
from django.utils.text import slugify
import itertools
from rest_framework.pagination import LimitOffsetPagination
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
from helper import generate_slug, get_field_name, get_permission_hierarchy
from ibedc_cms_backend.custompagination import CustomPaginatorClass
from location.models import EmsBusinessUnit
from config import CACHE_CONTROL
# from django.core.cache import cache

def fetch_and_cache_buids():
    # data = cache.get('buids')
    # if not data:
    data = list(EmsBusinessUnit.objects.filter().values('buid','name','state'))
        # cache.set('buids', data)
    return data

def search_for_buid(name,state,lst):
    for d in lst:
        if d["name"].lower() == name.lower() and d["state"].lower() == state.lower():
            return d["buid"]
        
        if d["name"].lower() == name.lower() and d['state'].lower()=='oyo' and state.lower() == 'ibadan':
            return d["buid"]
    return None

class SingleCustomer(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        accounttype = request.GET.get('accounttype')
        accountno = request.GET.get('accountno')
        if accounttype == 'prepaid':
            customer = EcmiCustomersNew.objects.filter(accountno__iexact=accountno).values(*ECMI_FIELDS) 
        else:
            customer = EmsCustomersNew.objects.filter(accountno__iexact=accountno).values(*EMS_FIELDS)
        if customer:
            response = {"status": True, "data": customer}
        else:
            response = {"status": False, "message": "No customer found with the provided account number."}
        return Response(response)
    
class TarrifCode(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        tariffid = request.GET.get('tariffid')
        accounttype = request.GET.get('accounttype')
        if accounttype == 'Prepaid':
            tarrif = EcmiTariff.objects.filter(tariffid=int(tariffid)).values().first() 
        elif accounttype == 'Postpaid':
            tarrif = EmsTariff.objects.filter(tariffid=int(tariffid)).values().first() 
      
        if tarrif:
            response = Response({"status": True, "data": tarrif})
            response.headers['Cache-Control'] = CACHE_CONTROL
            return response
        else:
            response = {"status": False, "message": "No tariff code found."}
            return Response(response)
    
        
class PrepaidCustomers(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        print("Location ====> ", field_name, "===> ", location) 
                
        if permission_hierarchy != generate_slug(user.permission_hierarchy):
            response = {"status":False, "message":"Hierarchy specified does not match legacy", "data":[]}
            return Response(response)
        
        self.custom_paginator = CustomPaginatorClass(PrepaidCustomers.pagination_class,request)
        customers = None
        total_customers = 0
        if start_date != end_date:
            if field_name is not None:
                if field_name == 'region' or 'state':
                    customers = EcmiCustomersNew.objects.filter(**{f"{field_name}__icontains": location}).filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
                elif field_name == 'buid':
                    customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": location}).filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
                    
                elif field_name == 'servicecenter':
                    customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location}).filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
            else:
                customers = EcmiCustomersNew.objects.filter().filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
        else:
            if field_name is not None:#For Non-HQ users
               
                if field_name == 'region' or field_name =='state':
                    location_customers = EcmiCustomersNew.objects.filter(**{f"{field_name}": location})
                    total_customers = location_customers.count()
                    customers = location_customers.values(*ECMI_FIELDS)[:1000]
                elif field_name == 'buid':
                    print(request.GET)
                    offset = request.GET.get('offset') or 0
                    location_customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": location}).order_by('-surname')#[offset:request.GET.get('offset',0)+request.GET.get('limit',100)]  #.filter(accountno='2451679551979')#
                    total_customers = location_customers.count()
                    
                    customers = location_customers.values(*ECMI_FIELDS)
                    
                elif field_name == 'servicecenter':
                    location_customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location}).order_by('-updated_at')
                    total_customers = location_customers.count()
                    customers = location_customers.values(*ECMI_FIELDS)            
            else:
                total_customers =EcmiCustomersNew.objects.all().count()
                customers = EcmiCustomersNew.objects.filter(state='Oyo').order_by('-updated_at').values(*ECMI_FIELDS)
        
        if customers:
            customers = self.custom_paginator.paginate_queryset(customers)
            response = self.custom_paginator.get_paginated_response(customers)
            response.data["status"] = True
            response.data["message"] = "ECMI Customers were successfully fetched"
            response.data["data"] = response.data.pop('results')
            response.data["total_customers"] = total_customers
        else:
            response = Response({"status": False, "message": "ECMI Customers could not be fetched", "data": []})
        
        response_cc = response
        response_cc.headers['Cache-Control'] = CACHE_CONTROL
        return response_cc
      
class PostpaidCustomers(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        print("Location ====> ", field_name, "===> ", location) 
                
        if permission_hierarchy != generate_slug(user.permission_hierarchy):
            response = {"status":False, "message":"Hierarchy specified does not match legacy", "data":[]}
            return Response(response)
        
        self.custom_paginator = CustomPaginatorClass(PrepaidCustomers.pagination_class,request)
        customers = None
        total_customers = 0
        
        if start_date != end_date:
            if field_name is not None:
                if field_name == 'region' or 'state':
                    customers = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": location}).filter(applicationdate__range=[start_date, end_date]).values(*EMS_FIELDS)
                elif field_name == 'buid':
                    customers = EmsCustomersNew.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": location}).filter(applicationdate__range=[start_date, end_date]).values(*EMS_FIELDS)
                elif field_name == 'servicecenter':
                    customers = EmsCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location}).filter(applicationdate__range=[start_date, end_date]).values(*EMS_FIELDS)
            else:
                customers = EmsCustomersNew.objects.filter().filter(applicationdate__range=[start_date, end_date]).values(*EMS_FIELDS)
                
        else:
            if field_name is not None:#For Non-HQ users
                
                if field_name == 'region' or 'state':
                    location_customers = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": location})
                    total_customers = location_customers.count()
                    customers = location_customers.values(*EMS_FIELDS)[:2000]
                    
                if field_name == 'buid':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(location, request.user.region, buids)
                    location_customersx = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": buid})
                    total_customers =location_customers.count()
                    customers = location_customersx.values(*EMS_FIELDS)[:2000]
                    
                if field_name == 'servicecenter':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(request.user.business_unit, request.user.region, buids)
                    location_customers = EmsCustomersNew.objects.filter(state=request.user.region).filter(buid=buid).filter(**{f"{field_name}__icontains": location})
                    total_customers = location_customers.count()
                    customers = location_customers.values(*EMS_FIELDS)            
            else:
                total_customers = EmsCustomersNew.objects.all().count()
                customers = EmsCustomersNew.objects.filter(state='Oyo')[:100024].values(*EMS_FIELDS)
                
        if customers:
            customers = self.custom_paginator.paginate_queryset(customers)
            response = self.custom_paginator.get_paginated_response(customers)
            response.data["status"] = True
            response.data["message"] = "EMS Customers were successfully fetched"
            response.data["data"] = response.data.pop('results')
            response.data["total_customers"] = total_customers
            response_cc = response
            response_cc.headers['Cache-Control'] = CACHE_CONTROL
        else:
            response = Response({"status": False, "message": "EMS Customers could not be fetched", "data": []})
        
        response_cc = response
        # response_cc.headers['Cache-Control'] = CACHE_CONTROL
        return response_cc
