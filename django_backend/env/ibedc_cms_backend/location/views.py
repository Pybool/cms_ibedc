# from django.db import connection
# from django.db.models import Count
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import LocationPermissions, CrmRegion, CrmBusinessHub, CrmServiceCentre
# from configurations import CACHE_CONTROL, PAGINATION_SETTINGS
# from helpers.permissions import Permissions
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

# from cmsadmin.models import LocationsPermissions
# class CustomerFilterView(APIView):
#     # authentication_classes = [JWTAuthenticationMiddleWare]
#     def get(self,request):
#         regions = LocationsPermissions.objects.filter().values('region').distinct() #.distinct('region)
#         return Response({'status':True,'regions':regions})


class LocationsView(APIView):
    
    def __init__(self):
        pass
    
    def get_locations_data(self, region):
        if region != None:
            locations_list = CrmRegion.objects.filter(name__iexact=region).values()
        else:
            locations_list = CrmRegion.objects.values()
        return locations_list
    
    def get_regions_data(self):
        regions_list = CrmRegion.objects.filter().values('id','name').distinct().order_by('name')
        return regions_list
    
    def get_business_unit_data(self, q):
        if q == '__all__':
            business_units = CrmBusinessHub.objects.values('id','name').distinct().order_by('name')
        else:
            region = get_object_or_404(CrmRegion,name__icontains=q)
            print("Region id ===> ", region.name, region.id)
            business_units = CrmBusinessHub.objects.filter(region__iexact=region.id).values('id','name').distinct().order_by('name')
        return business_units
    
    def get_service_center_data(self, q):
        if q == '__all__':
            service_centers = CrmServiceCentre.objects.values('id','name').distinct().order_by('name')
        else:
            business_hub = get_object_or_404(CrmBusinessHub,name__icontains=q)
            print("business_hub id ===> ", business_hub.name, business_hub.id)
            service_centers = CrmServiceCentre.objects.filter(business_hub__iexact=business_hub.id).values('id','name').distinct().order_by('name')
        return service_centers
    
    def search_locations(self, q):
        search_results = LocationPermissions.objects.filter(
            Q(region__icontains=q) | 
            Q(biz_hub__icontains=q) | 
            Q(service_center__icontains=q)
        ).values()
        
        return search_results
    
    
    def get(self, request, page=1):
        try:
            page = int(page)
            region = request.GET.get('region')
            # user_groups = Group.objects.all()
            locations_list_init = self.get_locations_data(region)
            paginator = Paginator(locations_list_init, PAGINATION_SETTINGS['LOCATIONS_PER_PAGE'])
            locations_list = paginator.get_page(page)
            dev_perm = Permissions.checkDeveloperPermissions(request.user)
            create_perm = Permissions.checkPermissions(request.user)
            caad_perm = Permissions.checkCaadApprovalPermissions(request.user)
            context = {
                'locations': locations_list,
                'dev_perm': dev_perm,
                'create_perm': create_perm,
                'caad_perm': caad_perm,
                'pager': locations_list,
                "can_approve": Permissions.checkCustomerApprovalPermissions(request.user),
                'locations':list(locations_list_init)
            }
            response_data = {"status": True, "data": context, "message": "success"}
            response = Response(response_data, safe=False)
            response['Cache-Control'] = CACHE_CONTROL
            return response
        except Exception as err:
            print("Error ", str(err))
            
class PermissionsHierarchyView(APIView):
    """ Examples:
    
        http://127.0.0.1:8000/api/v1/locations/getdata?hierarchy=business_unit&q=Oyo ==> Interpreted as get all business units in Oyo region
        http://127.0.0.1:8000/api/v1/locations/getdata?hierarchy=servicecenter&q=monatan==> Interpreted as get all service centers in Monatan bizhub"""
    def get(self, request,kw={}):
        
        hierarchy = request.GET.get('hierarchy', None)
        q = request.GET.get('q', '')
        print(kw)
        if kw.get('as_method'):
            hierarchy = kw.get('hierarchy', None)
            q = kw.get('q', '')
        try:
            data = {}
            if hierarchy == 'regions' or hierarchy == 'region':
                regions_list = LocationsView.get_regions_data(LocationsView)
                data['regions'] = regions_list
                
            elif hierarchy == 'business_unit':
                business_units = LocationsView.get_business_unit_data(LocationsView,q)
                data['business_units'] = business_units
            
            elif hierarchy == 'servicecenter':
                service_centers = LocationsView.get_service_center_data(LocationsView,q)
                data['service_centers'] = service_centers
                  
            response = {"status":True,"data":data,"message":"success"}
            if not kw.get('as_method'):
                return Response(response)
            return data
        
        except Exception as err:
            print("Error ",str(err))
            response = {"status":False,"error":str(err),"message":"failure"}  
            return Response(response)  

class CreateLocationView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            vals_user = {
                'region': data.get('regions'),
                'biz_hub': data.get('business_unit'),
                'servicecenter': data.get('servicecenter'),
                'service_center_address':data.get('service_center_address'),
                'buid':data.get('buid_code'),
                'created_by': request.user.email,
            }
            new_permission = LocationPermissions.objects.create(vals_user)
            
            response = {"status":True,"data":str(new_permission),"message":"Location was created successfully"}  
            return Response(response, status=200)
        
        except Exception as err:
            return Response({"status":False,"error":str(err),"message":"failure"}, status=404)
        
    # def put(self, request):
    #     data = request.data
    #     try:
    #         vals_location = {
    #             'region': data.get('regions'),
    #             'biz_hub': data.get('business_unit'),
    #             'servicecenter': data.get('servicecenter'),
    #             'service_center_address': data.get('service_center_address'),
    #             'buid': data.get('buid_code'),
    #         }
    #         edited_permission = get_object_or_404(Permissions, pk=data.get('id'))
    #         edited_permission.__dict__.update(vals_location)
    #         edited_permission.save()
    #         response = {"status": True, "data": str(edited_permission),
    #                     "message": "Location was edited successfully"}
    #         return Response(response, content_type='text/json;charset=utf-8')
    #     except Exception as err:
    #         response = {"status": False, "message": "Location was not saved successfully"}
    #         return Response(response, content_type='text/json;charset=utf-8')


# class LocationSearchView(APIView):
#     pagination_class = PageNumberPagination
#     page_size = PAGINATION_SETTINGS['LOCATIONS_PER_PAGE']

#     def get(self, request, format=None):
#         q = request.query_params.get('q', '')
#         page = request.query_params.get('page', 1)
#         try:
#             page = int(page)
#             user_groups = request.env['res.groups'].sudo().search([])
#             locations = self.search_locations(q)
#             total = len(locations)
#             pager = self.pagination_class()
#             paginated_locations = pager.paginate_queryset(locations, request)
#             dev_perm = Permissions.checkDeveloperPermissions(request.user)
#             create_perm = Permissions.checkPermissions(request.user)
#             caad_perm = Permissions.checkCaadApprovalPermissions(request.user)
#             data = {
#                 'groups': user_groups,
#                 'locations': paginated_locations,
#                 'dev_perm': dev_perm,
#                 'create_perm': create_perm,
#                 'caad_perm': caad_perm,
#                 'can_approve': Permissions.checkCustomerApprovalPermissions(request.user)
#             }
#             return pager.get_paginated_response(data)
#         except Exception as err:
#             print("locations error ", err)