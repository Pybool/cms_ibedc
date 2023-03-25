# import json
# from odoo import http
# from odoo.http import request, Response
# from ..settings import CACHE_CONTROL, PAGINATION_SETTINGS
# from odoo.addons.hr.models import main
# from ..utilitymethods.utility import Encryption, Permissions, Serializables, abbreviateName
from connection_executor import dict_fetch_all
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
import jwt, uuid, json
    
def get_locations_data(region):
    if region != None:
        query = """SELECT * FROM location_locationpermissions""" if region ==  '' else f"""SELECT * FROM location_locationpermissions WHERE region ilike '{region}'"""
    else:
        query = """SELECT * FROM location_locationpermissions"""
    return dict_fetch_all(query)

def get_regions_data():
    print(10000)
    query = """
                SELECT DISTINCT region FROM location_locationpermissions ORDER BY region;
            """
    print(query)
    print(dict_fetch_all(query))
    return dict_fetch_all(query)

def get_business_unit_data(q): 
    
    query = f"""
                SELECT DISTINCT biz_hub,buid FROM location_locationpermissions WHERE region = '{q}' ORDER BY biz_hub;
            """
            
    if q=='__all__':
        query = f"""
                SELECT DISTINCT biz_hub,buid FROM location_locationpermissions ORDER BY biz_hub;
                """
    return dict_fetch_all(query)

def get_service_center_data(q):
    query = f"""
                SELECT DISTINCT servicecenter FROM location_locationpermissions WHERE biz_hub = '{q}' ORDER BY servicecenter;
            """
    
    if q=='__all__':
        query = f"""
                SELECT DISTINCT servicecenter FROM location_locationpermissions ORDER BY servicecenter;
                """
    return dict_fetch_all(query)

def search_locations(q):
    query = f"""
                select 
                    *
                from 
                location_locationpermissions
                where upper(region) LIKE UPPER('%{q}%') OR
                upper(biz_hub) LIKE UPPER('%{q}%') OR
                upper(servicecenter) LIKE UPPER('%{q}%') ;
                """

    return dict_fetch_all(query)

# @http.route(['/cms/locations/', '/cms/locations/page/<int:page>'], website=True,auth='user')
# def locations_page(page=1,**kw):
#     try:
#         page = int(page)
#         print("Key ===> ", kw.get('region'))
#         #  kw['region'] = False if kw.get('region') == '' else False
#         user_groups = request.env['res.groups'].sudo().search([])
#         locations_list_init=get_locations_data(kw.get('region'))
#         pager = request.website.pager( 
#                                     url=f'/cms/locations',
#                                     total=len(locations_list_init),
#                                     page=page,
#                                     step=PAGINATION_SETTINGS['LOCATIONS_PER_PAGE'],
#                                     url_args= {}
#                                     )
#         offset = (page - 1) * PAGINATION_SETTINGS['LOCATIONS_PER_PAGE']
#         locations_list = locations_list_init[offset: offset + PAGINATION_SETTINGS['LOCATIONS_PER_PAGE']]
#         dev_perm = Permissions.checkDeveloperPermissions(http.request.env.user)
#         create_perm = Permissions.checkPermissions(http.request.env.user)
#         caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
#         if kw.get('http') == '1':
#             response = {"status":True,"data":locations_list_init,"message":"success"}
#             response =  Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')
#             response.headers['Cache-Control'] = CACHE_CONTROL
#             return response 
#         return request.render("cms_ibedc.locationpermissions",{'groups':user_groups,'locations':locations_list,'dev_perm':dev_perm,"create_perm":create_perm,"caad_perm":caad_perm,'pager':pager,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user)})
    
#     except Exception as err:
#         print("Error ",str(err))
#         return request.render("cms_ibedc.404notfound",{})


def get_hierarchy_data(request):
    try:
        q = request.GET.get('q','')
        hierarchy = request.GET.get("hierarchy")
        print("\n\n\n",hierarchy, q)
        data = {}
        if hierarchy == 'regions':
            regions_list = get_regions_data()
            data['regions'] = regions_list
            
        elif hierarchy == 'business_unit':
            business_units = get_business_unit_data(q)
            data['business_units'] = business_units
        
        elif hierarchy == 'servicecenter':
            service_centers = get_service_center_data(q)
            data['service_centers'] = service_centers
                
        response = json.dumps({"status":True,"data":data,"message":"success"})
        response =  HttpResponse(response)
        # response.headers['Cache-Control'] = CACHE_CONTROL
        return response    
    
    except Exception as err:
        print("Error ",str(err))
        response = {"status":False,"error":str(err),"message":"failure"}  
        return HttpResponse(response)  
    
# # @http.route(['/cms/save_locations/'], website=True,auth='user')
# def saveLocation(data,**kw):
    
#     data = json.loads(data)
#     try:
#         vals_user = {
#         'region': data.get('regions'),
#         'biz_hub': data.get('business_unit'),
#         'servicecenter': data.get('servicecenter'),
#         'service_center_address':data.get('service_center_address'),
#         'buid':data.get('buid_code'),
#         'created_by': http.request.env.user.login,
#         }
#         new_permission = http.request.env['locations.permissions'].sudo().create([vals_user])
        
#         response = {"status":True,"data":str(new_permission),"message":"Location was created successfully"}  
#         return Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')          
#     except Exception as err:
#         return request.render("cms_ibedc.404notfound",{})

# # @http.route(['/cms/edit_locations/'], website=True,auth='user')
# def editLocation(data,**kw):
    
#     data = json.loads(data)
#     print(data)
#     try:
#         vals_location = {
#         'region': data.get('regions'),
#         'biz_hub': data.get('business_unit'),
#         'servicecenter': data.get('servicecenter'),
#         'service_center_address':data.get('service_center_address'),
#         'buid':data.get('buid_code'),
#         }
#         edited_permission = http.request.env['locations.permissions'].sudo().browse(int(data.get('id')))
#         edited_permission.sudo().write(vals_location)
#         response = {"status":True,"data":str(edited_permission),"message":"Location was edited successfully"}  
#         return Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')          
#     except Exception as err:
#         response = {"status":False,"message":"Location was not saved successfully"}  
#         return Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')

# # @http.route(['/cms/search_locations/', '/cms/search_locations/page/<int:page>'], website=True,auth='user')
# def search_location(q,page=1,**kw):
#     try:
#         page = int(page)
#         user_groups = request.env['res.groups'].sudo().search([])
    
#         locations=search_locations(q)
#         pager = request.website.pager( 
#                                     url=f'/cms/search_locations',
#                                     total=len(locations),
#                                     page=page,
#                                     step=PAGINATION_SETTINGS['LOCATIONS_PER_PAGE'],
#                                     url_args= {'q':q}
#                                     )
#         offset = (page - 1) * PAGINATION_SETTINGS['LOCATIONS_PER_PAGE']
#         locations = locations[offset: offset + PAGINATION_SETTINGS['LOCATIONS_PER_PAGE']]
#         dev_perm = Permissions.checkDeveloperPermissions(http.request.env.user)
#         create_perm = Permissions.checkPermissions(http.request.env.user)
#         caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
#         return request.render("cms_ibedc.locationpermissions",{'groups':user_groups,'locations':locations,'dev_perm':dev_perm,"create_perm":create_perm,"caad_perm":caad_perm,'pager':pager,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user)})
#     except Exception as err:
#         print("locations error ", err)
