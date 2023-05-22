import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
# from ibedc_cms_backend.configurations import CACHE_CONTROL, PAGINATION_SETTINGS
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .fields import ECMI_FIELDS, EMS_FIELDS
from .models import EcmiCustomersNew, EmsCustomersNew
from authentication.models import User
from django.utils.text import slugify
import itertools
from location.models import EmsBusinessUnit
from helper import generate_slug, get_field_name, get_permission_hierarchy
from rest_framework.pagination import LimitOffsetPagination
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
from ibedc_cms_backend.custompagination import CustomPaginatorClass
import functools

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

def generate_slug(value):
    print("slug ", value)
    return value.replace(" ",'-').lower()

def get_field_name(permission_hierarchy):
    mapping = {
        'head-quarters': '',
        'region': 'state',
        'buisness-unit': 'buid',
        'service-center': 'servicecenter',
    }
    return mapping.get(permission_hierarchy, None)

def get_dictionary_query(search_dict):
    q_list = []

    # Loop through the dictionary and generate a Q object for each search term
    for field, term in search_dict.items():
        q = Q(**{f"{field}__icontains": term})
        q_list.append(q)
        
    search_query = Q()
    for q in q_list:
        search_query &= q
    
    return search_query
          
def ems_get_dictionary_query(request):
    q_list = []

    # Loop through the dictionary and generate a Q object for each search term
    for field, term in request.data.items():
        if field == 'buid':
            buids = fetch_and_cache_buids()
            try:
                region = request.data.get('state') if request.data.get('state') != None else request.user.region 
                buid = search_for_buid(term, region, buids)
            except:
                if request.user.region == 'granted':
                    buid = search_for_buid(term, region, buids,alt='name')
                else:
                    return Response({"status":False,"message":"A business hub might exist in a state outside your permission, select a state or region and try again"})
            buid = search_for_buid(term, region, buids)
            term = buid
        q = Q(**{f"{field}__icontains": term})
        q_list.append(q)
        
    search_query = Q()
    for q in q_list:
        search_query &= q
    
    return search_query
          
                   
class SearchPrepaidCustomers(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def post(self, request):
        
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        self.custom_paginator = CustomPaginatorClass(SearchPrepaidCustomers.pagination_class,request)
        customers = None
        total_customers = 0
        if(len(request.data.get('q')) > 0):
            search_q = request.data.get('q')[0]
            if request.data.get('fieldName') == 'names':
                """Handle cases where there are spaces in the search string"""  
                splited_search_q = search_q.split(" ")
                if len(splited_search_q) > 1:
                    queries = [Q(surname=item) | Q(firstname=item) | Q(othernames=item) for item in splited_search_q]
                    query = functools.reduce(lambda q1, q2: q1 | q2, queries)
                else:
                    query = Q(surname__icontains = search_q) |Q(firstname__icontains = search_q) | Q(othernames__icontains = search_q)
            else:
                splited_search_q = search_q.split(" ")
                if len(splited_search_q) > 1:
                    queries = [Q(**{f"{request.data.get('fieldName')}": item}) for item in splited_search_q]
                    query = functools.reduce(lambda q1, q2: q1 | q2, queries)
                else:
                    query = Q(**{f"{request.data.get('fieldName')}__icontains": search_q})
        
        else:
            return Response({"status":False,"message":"Invalid search parameter in request"})
        print(query, field_name,location)
        if(query):
            if field_name is not None:#For Non-HQ users
                    
                if field_name == 'region' or field_name == 'state':
                    search_location_customers = EcmiCustomersNew.objects.filter(**{f"{field_name}__icontains": location}).filter(query)
                    customers = search_location_customers.values(*ECMI_FIELDS)
                elif field_name == 'buid' or field_name == 'business-unit' or field_name == 'business_unit':
                    search_location_customers = EcmiCustomersNew.objects.filter(state__icontains=request.user.region).filter(**{f"{field_name}__icontains": location}).filter(query)
                    customers = search_location_customers.values(*ECMI_FIELDS)
                    
                elif field_name == 'servicecenter':
                    search_location_customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location}).filter(query)
                    customers = search_location_customers.values(*ECMI_FIELDS)            
            else:
                total_customers =EcmiCustomersNew.objects.filter(query).count()
                customers = EcmiCustomersNew.objects.filter(query).values(*ECMI_FIELDS)
                print(customers)
            
            if customers:
                customers = self.custom_paginator.paginate_queryset(customers)
                response = self.custom_paginator.get_paginated_response(customers)
                response.data["status"] = True
                response.data["message"] = "Request complted successfully"
                response.data["data"] = response.data.pop('results')
                response.data["total_customers"] = total_customers
            else:
                response = Response({"status": False, "message": "No search results were found for your search", "data": []})
        else:
            response = Response({"status":False,"message":"Could not process an invalid request"})
            
        return response

      
class SearchPostpaidCustomers(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def post(self, request):
        
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        self.custom_paginator = CustomPaginatorClass(SearchPrepaidCustomers.pagination_class,request)
        customers = None
        total_customers = 0
        if(len(request.data.get('q')) > 0):
            search_q = request.data.get('q')[0]
            if request.data.get('fieldName') == 'names':
                """Handle cases where there are spaces in the search string"""  
                splited_search_q = search_q.split(" ")
                if len(splited_search_q) > 1:
                    queries = [Q(surname=item) | Q(firstname=item) | Q(othernames=item) for item in splited_search_q]
                    query = functools.reduce(lambda q1, q2: q1 | q2, queries)
                else:
                    query = Q(surname__icontains = search_q) |Q(firstname__icontains = search_q) | Q(othernames__icontains = search_q)
            else:
                splited_search_q = search_q.split(" ")
                if len(splited_search_q) > 1:
                    queries = [Q(**{f"{request.data.get('fieldName')}": item}) for item in splited_search_q]
                    query = functools.reduce(lambda q1, q2: q1 | q2, queries)
                else:
                    if request.data.get('fieldName') == 'buid': #If the location searched is busines Unit fid the code and use it to query
                        buids = fetch_and_cache_buids()
                        if request.user.region != 'granted':
                            search_q = search_for_buid(search_q, request.user.region, buids)
                        else:
                            search_q = search_for_buid(search_q, '', buids,alt='name')
                    query = Q(**{f"{request.data.get('fieldName')}__icontains": search_q})
        
        else:
            return Response({"status":False,"message":"Invalid search parameter in request"})
        print(query)
        if(query):
            if field_name is not None:#For Non-HQ users
                    
                if field_name == 'region':
                    search_location_customers = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": location}).filter(query).count()
                    customers = search_location_customers.values(*EMS_FIELDS)
                elif field_name == 'buid':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(location, request.user.region, buids)
                    search_location_customers = EmsCustomersNew.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": buid}).filter(query)
                    customers = search_location_customers.values(*EMS_FIELDS)
                    
                elif field_name == 'servicecenter':
                    search_location_customers = EmsCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location}).filter(query)
                    customers = search_location_customers.values(*EMS_FIELDS)            
            else:
                total_customers =EmsCustomersNew.objects.filter(query).count()
                customers = EmsCustomersNew.objects.filter(query).values(*EMS_FIELDS)
            
            if customers:
                customers = self.custom_paginator.paginate_queryset(customers)
                response = self.custom_paginator.get_paginated_response(customers)
                response.data["status"] = True
                response.data["message"] = "Request complted successfully"
                response.data["data"] = response.data.pop('results')
                response.data["total_customers"] = total_customers
            else:
                response = Response({"status": False, "message": "Ems Customers could not be fetched", "data": []})
        else:
            response = Response({"status":False,"message":"Could not process an invalid request"})
            
        return response


class AdvancedSearchPrepaidCustomers(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def post(self, request):
        
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        self.custom_paginator = CustomPaginatorClass(SearchPrepaidCustomers.pagination_class,request)
        customers = None
        total_customers = 0
        print('Dual Mode----> ',type(request.GET.get('dual')))
        q = get_dictionary_query(request.data)
        print("Cobined Q ==> ", q)
        if(len(request.data.keys()) > 0):
        
            if field_name is not None:#For Non-HQ users
                    
                if field_name == 'region':
                    search_location_customers = EcmiCustomersNew.objects.filter(**{f"{field_name}__icontains": location}).filter(**request.data).count()
                    customers = search_location_customers.values(*ECMI_FIELDS)
                elif field_name == 'buid':
                    search_location_customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": location}).filter(**request.data)
                    customers = search_location_customers.values(*ECMI_FIELDS)
                    
                elif field_name == 'servicecenter':
                    search_location_customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location}).filter(**request.data)
                    customers = search_location_customers.values(*ECMI_FIELDS)            
            else:
                total_customers =EcmiCustomersNew.objects.filter(q).count()
                # customers = EcmiCustomersNew.objects.filter(**request.data).values(*ECMI_FIELDS)
                customers = EcmiCustomersNew.objects.filter(q).values(*ECMI_FIELDS)

            
            if customers:
                customers = self.custom_paginator.paginate_queryset(customers)
                response = self.custom_paginator.get_paginated_response(customers)
                response.data["status"] = True
                response.data["message"] = "Request complted successfully"
                response.data["data"] = response.data.pop('results')
                response.data["total_customers"] = total_customers
            else:
                response = Response({"status": False, "message": "ECMI Customers could not be fetched", "data": []})
        else:
            response = Response({"status":False,"message":"Could not process an invalid request"})
            
        return response


class AdvancedSearchPostpaidCustomers(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    pagination_class = LimitOffsetPagination
    def post(self, request):
        
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name, location = get_permission_hierarchy(request)
        self.custom_paginator = CustomPaginatorClass(SearchPrepaidCustomers.pagination_class,request)
        customers = None
        total_customers = 0
        print('Dual Mode----> ',type(request.GET.get('dual')))
        q = ems_get_dictionary_query(request)
        print("Cobined Q ==> ", q)
        if(len(request.data.keys()) > 0):
        
            if field_name is not None:#For Non-HQ users
                    
                if field_name == 'region':
                    search_location_customers = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": location}).filter(**request.data).count()
                    customers = search_location_customers.values(*EMS_FIELDS)
                elif field_name == 'buid':
                    buids = fetch_and_cache_buids()
                    buid = search_for_buid(location, request.user.region, buids)
                    search_location_customers = EmsCustomersNew.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": buid}).filter(**request.data)
                    customers = search_location_customers.values(*EMS_FIELDS)
                    
                elif field_name == 'servicecenter':
                    search_location_customers = EmsCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location}).filter(**request.data)
                    customers = search_location_customers.values(*EMS_FIELDS)            
            else:
                total_customers =EmsCustomersNew.objects.filter(q).count()
                customers = EmsCustomersNew.objects.filter(q).values(*EMS_FIELDS)

            
            if customers:
                customers = self.custom_paginator.paginate_queryset(customers)
                response = self.custom_paginator.get_paginated_response(customers)
                response.data["status"] = True
                response.data["message"] = "Request complted successfully"
                response.data["data"] = response.data.pop('results')
                response.data["total_customers"] = total_customers
            else:
                response = Response({"status": False, "message": "EMS Customers could not be fetched", "data": []})
        else:
            response = Response({"status":False,"message":"Could not process an invalid request"})
            
        return response

