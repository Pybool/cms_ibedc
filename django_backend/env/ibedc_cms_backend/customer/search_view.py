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

class SinglePrepaidCustomer(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name = get_field_name(permission_hierarchy)
        location = permission_hierarchy.replace('-', '_')
        
class SinglePostpaidCustomer(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email=request.user.email)
        field_name = get_field_name(permission_hierarchy)
        location = permission_hierarchy.replace('-', '_')       

class SearchPrepaidCustomers(APIView):
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
        
        limit = 100
        paginator = LimitOffsetPagination()
        paginator.default_limit = limit
        customers = None
        if start_date != end_date:
            if field_name is not None:
                customers = EcmiCustomersNew.objects.filter(**{f"{field_name}__icontains": getattr(user, location)}).filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
            else:
                customers = EcmiCustomersNew.objects.filter().filter(opendate__range=[start_date, end_date]).values(*ECMI_FIELDS)
        else:
            if field_name is not None:
                customers = EcmiCustomersNew.objects.filter(**{f"{field_name}__icontains": getattr(user, location)}).values(*ECMI_FIELDS)
            else:
                customers = EcmiCustomersNew.objects.filter().values(*ECMI_FIELDS)
        
        if customers:
            result_page = paginator.paginate_queryset(customers, request)
            next_page_link = paginator.get_next_link()
            previous_page_link = paginator.get_previous_link()
            # last_page_link = paginator.get_last_link()
            response = {"status": True, "message": "ECMI Customers were successfully fetched", "data": result_page, "next": next_page_link, "previous": previous_page_link, "last": 'last_page_link'}
        else:
            response = {"status": False, "message": "ECMI Customers could not be fetched", "data": []}
        
        print(response)
        return Response(response)


      
class SearchPostpaidCustomers(APIView):
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
        
        limit = 10000
        paginator = LimitOffsetPagination()
        paginator.default_limit = limit
        customers = None
        if start_date != end_date:
            if field_name is not None:
                customers = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": getattr(user, location)}).filter(applicationdate__range=[start_date, end_date]).values(*EMS_FIELDS)
            else:
                customers = EmsCustomersNew.objects.filter().filter(applicationdate__range=[start_date, end_date]).values(*EMS_FIELDS)
        else:
            if field_name is not None:
                customers = EmsCustomersNew.objects.filter(**{f"{field_name}__icontains": getattr(user, location)}).values(*EMS_FIELDS)[:10000]
                print(len(customers))
            else:
                customers = EmsCustomersNew.objects.filter().values(*EMS_FIELDS)
        
        if customers:
            result_page = paginator.paginate_queryset(customers, request)
            next_page_link = paginator.get_next_link()
            previous_page_link = paginator.get_previous_link()
            # last_page_link = paginator.get_last_link()
            response = {"status": True, "message": "Ems Customers were successfully fetched", "data": result_page, "next": next_page_link, "previous": previous_page_link, "last": 'last_page_link'}
        else:
            response = {"status": False, "message": "Ems Customers could not be fetched", "data": []}
        
        return Response(response)
    
