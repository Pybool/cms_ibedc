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
from rest_framework.pagination import LimitOffsetPagination
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
from helper import generate_slug, get_field_name, get_permission_hierarchy
from ibedc_cms_backend.custompagination import CustomPaginatorClass

class SingleCustomer(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        accounttype = request.GET.get('accounttype')
        accountno = request.GET.get('accountno')
        if accounttype == 'postpaid':
            customer = EmsCustomersNew.objects.filter(accountno__iexact=accountno).values(*EMS_FIELDS)
        else:
            customer = EcmiCustomersNew.objects.filter(accountno__iexact=accountno).values(*ECMI_FIELDS) 
        if customer:
            response = {"status": True, "data": customer}
        else:
            response = {"status": False, "message": "No customer found with the provided account number."}
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
                if field_name == 'region':
                    customers = EcmiCustomersNew.objects.filter(**{f"{field_name}__icontains": location}).filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
                elif field_name == 'buid':
                    
                    customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": location}).filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
                    
                elif field_name == 'servicecenter':
                    customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location}).filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
            else:
                customers = EcmiCustomersNew.objects.filter().filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
        else:
            if field_name is not None:#For Non-HQ users
                
                if field_name == 'region':
                    location_customers = EcmiCustomersNew.objects.filter(**{f"{field_name}__icontains": location}).count()
                    total_customers = location_customers.count()
                    customers = location_customers.values(*ECMI_FIELDS)
                elif field_name == 'buid':
                    location_customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(**{f"{field_name}__icontains": location})
                    total_customers = location_customers.count()
                    customers = location_customers.values(*ECMI_FIELDS)
                    
                elif field_name == 'servicecenter':
                    location_customers = EcmiCustomersNew.objects.filter(state=request.user.region).filter(buid=request.user.business_unit).filter(**{f"{field_name}__icontains": location})
                    total_customers = location_customers.count()
                    customers = location_customers.values(*ECMI_FIELDS)            
            else:
                total_customers = EcmiCustomersNew.objects.all().count()
                customers = EcmiCustomersNew.objects.filter(state='Oyo').values(*ECMI_FIELDS)
        
        if customers:
            customers = self.custom_paginator.paginate_queryset(customers)
            print("/n/nCustomers ===> ",self.custom_paginator.get_paginated_response(customers))
            response = self.custom_paginator.get_paginated_response(customers)
            response.data["status"] = True
            response.data["message"] = "ECMI Customers were successfully fetched"
            response.data["data"] = response.data.pop('results')
            response.data["total_customers"] = total_customers
        else:
            response = Response({"status": False, "message": "ECMI Customers could not be fetched", "data": []})
        
        return response
      
class PostpaidCustomers(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name = get_field_name(permission_hierarchy)
        location = permission_hierarchy.replace('-', '_')
        
        print("Location ====> ", field_name, getattr(user, location))
        
        if permission_hierarchy != generate_slug(user.permission_hierarchy):
            response = {"status":False, "message":"Hierarchy specified does not match legacy", "data":[]}
            return Response(response)
        
        limit = 250
        paginator = LimitOffsetPagination()
        paginator.default_limit = limit
        customers = None
        total_customers = EmsCustomersNew.objects.all().count()
        if start_date != end_date:
            if field_name is not None:
                customers = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": getattr(user, location)}).filter(applicationdate__range=[start_date, end_date]).values(*EMS_FIELDS)
            else:
                customers = EmsCustomersNew.objects.filter().filter(applicationdate__range=[start_date, end_date]).values(*EMS_FIELDS)
        else:
            if field_name is not None:
                customers = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": getattr(user, location)}).values(*EMS_FIELDS)[:1000]
                print(len(customers))
            else:
                customers = EmsCustomersNew.objects.filter().values(*EMS_FIELDS)
        
        if customers:
            result_page = paginator.paginate_queryset(customers, request)
            next_page_link = paginator.get_next_link()
            previous_page_link = paginator.get_previous_link()
            # last_page_link = paginator.get_last_link()
            response = {"status": True, "message": "Ems Customers were successfully fetched", "data": result_page, "total_customers":total_customers, "next": next_page_link, "previous": previous_page_link, "last": 'last_page_link'}
        else:
            response = {"status": False, "message": "Ems Customers could not be fetched", "data": []}
        
        return Response(response)
