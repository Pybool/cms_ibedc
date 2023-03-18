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
from rest_framework.pagination import LimitOffsetPagination
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
from connection_executor import dict_fetch_all
from .raw_queries import *
from helper import generate_slug, get_field_name



class SingleCustomerPayments(APIView):
    # authentication_classes = [JWTAuthenticationMiddleWare]
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
            response = {"status": False, "message": "No customer payments found with the provided account number."}
        return Response(response)


class CustomerPayments(APIView):
    # authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        page_no = str(request.GET.get('page', 1))
        page_size = str(request.GET.get('page_size', 10))
        permission_hierarchy = generate_slug(request.GET.get('permission_hierarchy'))
        user = get_object_or_404(User, email='devops@plexada.com')
        field_name = get_field_name(permission_hierarchy)
        location = permission_hierarchy.replace('-', '_')
        
        print("Location ====> ", field_name, getattr(user, location))
        
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
        