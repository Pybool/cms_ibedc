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
    # authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        accountno = request.GET.get('accountno')
        page_no = str(request.GET.get('page', 1))
        page_size = str(request.GET.get('page_size', 10))
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email='devops@plexada.com')
        field_name = get_field_name(permission_hierarchy)
        location = permission_hierarchy.replace('-', '_')
                
        if permission_hierarchy != generate_slug(user.permission_hierarchy):
            response = {"status":False, "message":"Hierarchy specified does not match legacy", "data":[]}
            return Response(response)
        
        if permission_hierarchy != '':
            query =  BILLING_HISTORY_HIERARCHY\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\
                        .replace("#hierarchy#",field_name)\
                        .replace("#hierarchy_value#",getattr(user, location))
        else:
            query =  BILLING_HISTORY_NO_HIERARCHY\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)\

        bills = dict_fetch_all(query)#EmsBills.objects.filter(accountno__iexact=accountno).all().order_by('id')[:10]
        if bills:
            response = {"status": True, "count":len(bills), "data": bills}
        else:
            response = {"status": False, "message": "No customer bills found with the provided account number."}
        return Response(response)
        