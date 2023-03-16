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



class SingleCustomerMetering(APIView):
    # authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        accountno = request.GET.get('accountno')
        accounttype = request.GET.get('accounttype')
        page_no = str(request.GET.get('page', 1))
        page_size = str(request.GET.get('page_size', 10))
        if accounttype == 'postpaid':
            query =  SINGLE_EMS_CUSTTOMER_METERING_INFO\
                        .replace("#AccountNo#",accountno)\
                        .replace("#page_size#",page_size)\
                        .replace("#page_no#",page_no)
        else:
            query =  SINGLE_ECMI_CUSTTOMER_METERING_INFO\
                        .replace("#AccountNo#",accountno)
        print(query)
        payments = dict_fetch_all(query)#Emspayments.objects.filter(accountno__iexact=accountno).all().order_by('id')[:10]
        if payments:
            response = {"status": True, "count":0, "data": payments}
        else:
            response = {"status": False, "message": "No customer payments found with the provided account number."}
        return Response(response)

