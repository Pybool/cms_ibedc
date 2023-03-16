from django.shortcuts import render

# Create your views here.
from email.policy import default
import json
import re, random
import locale, datetime
from string import Template
import logging

from .users import checkUid
_logger = logging.getLogger(__name__)
from .kyc import check_kyc_compliance
from .locations_permissions import LocationsView
from .filter_query_constructor import FilterQueryConstructor
from .dynamic_renderer.customers import customer_table_rows, get_name_cell
from odoo import http
from odoo.http import request, Response
from ..utilitymethods.utility import Encryption, Permissions, Serializables, abbreviateName
from ..models.customer_profile import BaseDeclarative
from ..utilitymethods.utility  import TransientFields 
from ..utilitymethods.utility import Encryption, User
from ..sqlqueryselectors.customers_query_selectors import QuerySelectors
from ..settings import ASYNC_CUSTOMER_CACHE_CONTROL, ASYNC_CUSTOMER_CACHE_CONTROL_SHORT, CACHE_CONTROL, QUERY_SETTINGS, PAGINATION_SETTINGS
from .config import states
from .settings import SettingsView

class Billing(object):
    pass

class CustomerUtils(object):
    
    def __init__(self,http_request):
        self.http_request = http_request
        
    def get_users_list(self):
        users_lst = []
        ulst = """select id, partner_id from res_users;"""
        self.http_request.cr.execute(ulst)
        Users_id_list = request.cr.fetchall()
        for id in Users_id_list:
            users_lst.append(id[0])
            users_lst.append(id[1])
        return users_lst
    
    def getSingleCustomer(self,accountno):
        self.accountno = accountno
        try:
            Customers = self.http_request.env['res.partner']
            service_center_user = self.http_request.env.user.is_servicecenter_user() 
            business_unit_user = self.http_request.env.user.is_businesshub_level_user()
            regional_user = self.http_request.env.user.is_regional_level_user()
            hq_user = self.http_request.env.user.is_headquarters_level_user()
            permissions_dict = {'state':self.http_request.env.user.region,'buid':self.http_request.env.user.business_unit,'servicecenter':self.http_request.env.user.servicecenter,'bucode':self.http_request.env.user.bucode}

            if hq_user:
                key = 'hq'
                query = f""" 
                            SELECT 
                                    {QuerySelectors.queryselectors_cust},
                                    billing_history.total_due as outstanding_amnt,
                                    M.unique_code AS map_id
                                    
                                FROM
                                    res_partner
                                LEFT OUTER JOIN res_country_state on res_partner.state_id = res_country_state.id
                                LEFT OUTER JOIN billing_history on billing_history.accountno = res_partner.accountno
                                LEFT OUTER JOIN msms_meter_details ON res_partner.meter_number = msms_meter_details.meter_number
                                LEFT OUTER JOIN (SELECT * FROM gis_distribution_substation_11kv_415
                                                union 
                                                SELECT * FROM gis_distribution_substation_33kv_415
                                                ) as gis_distribution_substation_agg
                                    on res_partner.dss_id = gis_distribution_substation_agg.assetid
                                LEFT OUTER JOIN msms_customers AS M ON M.previous_account_number = res_partner.accountno
                                WHERE res_partner.accountno = '{self.accountno}'
                                ORDER BY res_partner.name
                                
                            ;"""
                
            if regional_user or business_unit_user or service_center_user: 
                if regional_user :
                    key = 'state'
                    PERMISSION = f"""{key} ilike '{permissions_dict[key]}'"""
                elif business_unit_user:
                    key = 'buid' 
                    PERMISSION = f"""{key} ilike ('{permissions_dict[key]}','{permissions_dict["bucode"]}')"""
                elif service_center_user:
                    key = 'servicecenter'
                    PERMISSION = f"""{key} ilike '{permissions_dict[key]}'"""
                    
                query = f""" 
                            SELECT 
                                    {QuerySelectors.queryselectors_cust},
                                    billing_history.total_due as outstanding_amnt,
                                    M.unique_code AS map_id
                                    
                                FROM

                                    res_partner
                                    
                                LEFT OUTER JOIN billing_history on billing_history.accountno = res_partner.accountno
                                LEFT OUTER JOIN msms_meter_details ON res_partner.meter_number = msms_meter_details.meter_number
                                LEFT OUTER JOIN msms_customers AS M ON M.previous_account_number = res_partner.accountno
                                WHERE res_partner.accountno = '{self.accountno}' AND res_partner.{PERMISSION} 
                                ORDER BY res_partner.id
                                
                            ;"""
                        
        
            self.http_request.cr.execute(query)
            customers_list = request.cr.dictfetchall()
            print(query)
            _logger.info(f"{query}")
            print("==> ",customers_list)
            return self.makeUrl(Customers,customers_list,True) 
        except Exception as err:
            print(str)
    
    def getMinifiedSingleCustomer(self,accountno,edit_form):
        self.accountno = accountno
        try:
            # Customers = self.http_request.env['res.partner']
            service_center_user = self.http_request.env.user.is_servicecenter_user() 
            business_unit_user = self.http_request.env.user.is_businesshub_level_user()
            regional_user = self.http_request.env.user.is_regional_level_user()
            hq_user = self.http_request.env.user.is_headquarters_level_user()
            permissions_dict = {'state':self.http_request.env.user.region,'buid':self.http_request.env.user.business_unit,'servicecenter':self.http_request.env.user.servicecenter,'bucode':self.http_request.env.user.bucode}
            
            if hq_user:
                key = 'hq'
                if edit_form == '0':
                    query = f""" 
                                SELECT 
                                        {QuerySelectors.queryselectors_cust_min}
                                    FROM
                                        res_partner
                                    WHERE res_partner.accountno = '{self.accountno}'
                                ;"""
                elif edit_form == '1':
                    query = f""" 
                                SELECT 
                                    {QuerySelectors.queryselectors_cust_min},
                                    dss_data,feeder_data
                                FROM

                                    res_partner,
                                    coalesce((select concat(dss_11kv_415v_name ,' .*. ', dss_11kv_415v_owner) from gis_distribution_substation_11kv_415 where assetid = (select upper(dss_id) from res_partner where accountno = '{self.accountno}')
                                        UNION
                                        select concat(dss_33kv_415v_name ,' .*. ', dss_33kv_415v_owner) from gis_distribution_substation_33kv_415 where assetid = (select upper(dss_id) from res_partner where accountno = '{self.accountno}')
                                    ),'') as dss_data,
                                    coalesce((select concat(f11kv_feeder_name ,' .*. ', asset_type) from gis_ibedc_11kv_feeder where assetid = (select upper(feederid) from res_partner where accountno = '{self.accountno}')
                                        UNION
                                        select concat(f33kv_feeder_name ,' .*. ', asset_type) from gis_ibedc_33kv_feeder where assetid = (select upper(feederid) from res_partner where accountno = '{self.accountno}')
                                    ),'') as feeder_data
                                    WHERE res_partner.accountno = '{self.accountno}'
                                    
                            ;"""
            # LEFT OUTER JOIN gis_distribution_substation_11kv_415 AS D11 ON D11.assetid = E.dss_id
            #                 LEFT OUTER JOIN gis_service_units AS S ON S.name = D11.dss_11kv_415v_owner 
            if regional_user or business_unit_user or service_center_user: 
                if regional_user :
                    key = 'state'
                    PERMISSION = f"""{key} ilike '{permissions_dict[key]}'"""
                elif business_unit_user:
                    key = 'buid' 
                    PERMISSION = f"""{key} ilike ('{permissions_dict[key]}','{permissions_dict["bucode"]}')"""
                elif service_center_user:
                    key = 'servicecenter'
                    PERMISSION = f"""{key} ilike '{permissions_dict[key]}'"""
                print("Edit form====>  ",edit_form)
                if edit_form == '0':
                    query = f""" 
                                SELECT 
                                        {QuerySelectors.queryselectors_cust_min}
                                        
                                    FROM

                                        res_partner
                                    WHERE res_partner.accountno = '{self.accountno}' AND LOWER(res_partner.{PERMISSION} 
                                ;"""
                                
                elif edit_form == '1':
                    query = f""" 
                                SELECT 
                                    {QuerySelectors.queryselectors_cust_min},
                                    dss_data,feeder_data
                                FROM
                                res_partner,
                                coalesce((select concat(dss_11kv_415v_name ,' .*. ', dss_11kv_415v_owner) from gis_distribution_substation_11kv_415 where assetid = (select upper(dss_id) from res_partner where accountno = '{self.accountno}')
                                    UNION
                                    select concat(dss_33kv_415v_name ,' .*. ', dss_33kv_415v_owner) from gis_distribution_substation_33kv_415 where assetid = (select upper(dss_id) from res_partner where accountno = '{self.accountno}')
                                ),'') as dss_data,
                                coalesce((select concat(f11kv_feeder_name ,' .*. ', asset_type) from gis_ibedc_11kv_feeder where assetid = (select upper(feederid) from res_partner where accountno = '{self.accountno}')
                                    UNION
                                    select concat(f33kv_feeder_name ,' .*. ', asset_type) from gis_ibedc_33kv_feeder where assetid = (select upper(feederid) from res_partner where accountno = '{self.accountno}')
                                ),'') as feeder_data
                                WHERE res_partner.accountno = '{self.accountno}' AND res_partner.{PERMISSION} 
                                ;"""
                                
            print("Custom query ", query)
            self.http_request.cr.execute(query)
            customers_list = request.cr.dictfetchall()[0]
            print("customer edit data ===> ",customers_list)
            if customers_list:
                if customers_list['buid'] != None:
                    bizhub = self.get_business_unit(customers_list['buid'].upper())
                    customers_list['buid'] =  bizhub if bizhub !=0 else customers_list['buid']
            return customers_list
        except Exception as err:
            print("EDit err ", err)
            return False
    

    def get_business_unit(self,buid):
        try:
            self.user = self.http_request.env['res.users'].sudo().browse(request.session.uid)
            self.business_units = LocationsView.get_business_unit_data(LocationsView,q=str(self.user.region))
            result = list(filter(lambda biz_unit: biz_unit['buid'].upper() == buid, self.business_units))[0].get('biz_hub')
            return result
        except Exception as e:
            return 0
            
    def makeUrl(self,Customers,customers_list,search=False,browse=True,accounttype=''):
        users_lst = self.get_users_list()
        total_customers = 0
        service_center_user = self.http_request.env.user.is_servicecenter_user()
        business_unit_user = self.http_request.env.user.is_businesshub_level_user()
        regional_user = self.http_request.env.user.is_regional_level_user()
        hq_user = self.http_request.env.user.is_headquarters_level_user()
        permissions_dict = {'state':self.http_request.env.user.region,'buid':self.http_request.env.user.business_unit,'servicecenter':self.http_request.env.user.servicecenter,'bucode':self.http_request.env.user.bucode,'hq':'GRANTED'}
        
        if regional_user :
            key = 'state'
        elif business_unit_user:
            key = 'buid' 
        elif service_center_user:
            key = 'servicecenter'
        elif hq_user:
            key = 'hq'
            
        if search==False:
            
            if hq_user:
                key = 'hq'
                count_query = f"""SELECT COUNT(1) FROM res_partner WHERE accounttype ='{accounttype}' and  res_partner.accountno is not null and res_partner.accountno != ''"""

            if regional_user or business_unit_user or service_center_user: 
                if regional_user :
                    key = 'state'
                    PERMISSION = f"""{key} ilike '{permissions_dict[key]}'"""
                elif business_unit_user:
                    key = 'buid' 
                    PERMISSION = f"""{key} in ('{permissions_dict[key]}','{permissions_dict["bucode"]}')"""
                elif service_center_user:
                    key = 'servicecenter'
                    PERMISSION = f"""{key} ilike '{permissions_dict[key]}'"""
                
                count_query = f"""SELECT COUNT(1) FROM res_partner WHERE accounttype ='{accounttype}' and  res_partner.{PERMISSION}"""
            print(count_query)       
            self.http_request.cr.execute(count_query)
            total_customers =  request.cr.fetchall()[0][0]
        else:
            try:
                total_customers = int(customers_list[0]['count'])
            except Exception as e:
                if 'list index out of range' in str(e):
                    return Customers, customers_list, 0, 0
                
        megalist = []
        if customers_list:
            for single_dict in customers_list:
                kyc_compliance = check_kyc_compliance(single_dict)
                single_dict['kyc'] = kyc_compliance
                # if single_dict['buid'] != None:
                #     bizhub = self.get_business_unit(single_dict['buid'].upper())
                #     single_dict['buid'] =  bizhub if bizhub !=0 else single_dict['buid']
                megalist.append(single_dict)
                if browse == True:
                    Customers += self.http_request.env['res.partner'].sudo().browse(single_dict['id'])
        if browse == True:
            return Customers,megalist,total_customers,len(megalist),key,permissions_dict
        else:
            return megalist,total_customers,len(megalist),key,permissions_dict

class CustomersView(http.Controller):
    
    def __init__(self):
        
        self.abbreviateName = abbreviateName
        
    def view_initializer(self):
        self.granted = 0
        self.business_units = 0
        self.regions_flag = 0 
        self.user = request.env['res.users'].sudo().browse(request.session.uid)
        self.regions = LocationsView.get_regions_data(LocationsView)
        self.business_units = LocationsView.get_business_unit_data(LocationsView,q=str(self.user.region))
        self.service_centers = LocationsView.get_service_center_data(LocationsView,q=str(self.user.business_unit))
        self.biz_hub_list = []
        self.service_centers_list = []
        self.bizhub = []
        self.service_centers = []
        self.regions = []
        self.regions_list = []
        self.http_request = http.request
        self.service_center_user = self.http_request.env.user.is_servicecenter_user()
        self.business_unit_user = self.http_request.env.user.is_businesshub_level_user()
        self.regional_user = self.http_request.env.user.is_regional_level_user()
        self.hq_user = self.http_request.env.user.is_headquarters_level_user()
        self.permissions_dict = {'state':self.http_request.env.user.region,'buid':self.http_request.env.user.business_unit,'servicecenter':self.http_request.env.user.servicecenter,'bucode':self.http_request.env.user.bucode,'hq':'GRANTED'}
        
        if self.hq_user :
            self.key = 'hq'            
        elif self.regional_user :
            self.key = 'state'
            self.PERMISSION = f"""{self.key} ilike '{self.permissions_dict[self.key]}'"""
        elif self.business_unit_user:
            self.key = 'buid' 
            self.PERMISSION = f"""{self.key} in ('{self.permissions_dict[self.key]}','{self.permissions_dict["bucode"]}')"""
        elif self.service_center_user:
            self.key = 'servicecenter'
            self.PERMISSION = f"""{self.key} ilike '{self.permissions_dict[self.key]}'"""
        
        # print("=========================> ",self.regional_user,self.business_unit_user,self.service_center_user)
    
    def get_colors(self):
        # color_lst = ['#95ac12', '#56e29b', '#200a87', '#317524', '#e0e415', '#32c655', '#a5cb0c', '#f16820', '#eedd32', '#626447', '#eed4d5', '#034ef8', '#99626d', '#f4508b', '#421254', '#8ddcd6', '#4ed9da', '#3dd660', '#b76494', '#c8b3ae']
        get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))
        rand_colour = [random.choice(get_colors(50)) for i in range(1)]
        return rand_colour
  
    def sort_locations(self):
        self.user = request.env['res.users'].sudo().browse(request.session.uid)
        if self.user.is_servicecenter_user():
            self.service_centers = 0
            return [], [], []
        if self.user.is_businesshub_level_user():
            self.business_units = 1
            query = (
                f"SELECT DISTINCT servicecenter FROM location_locationpermissions "
                f"WHERE biz_hub = '{self.user.business_unit}'"
            )
            http.request.cr.execute(query)
            locations = request.cr.dictfetchall()
            self.service_centers_list = [location['servicecenter'] for location in locations]
        if self.user.is_regional_level_user():
            self.regions_flag = 1
            query = (
                f"SELECT biz_hub, servicecenter FROM location_locationpermissions "
                f"WHERE region = '{self.user.region}'"
            )
            http.request.cr.execute(query)
            locations = request.cr.dictfetchall()
            self.biz_hub_list = [location['biz_hub'] for location in locations]
            self.service_centers_list = [location['servicecenter'] for location in locations]
        if self.user.is_headquarters_level_user():
            self.granted = 1
            query = "SELECT biz_hub, servicecenter, region FROM location_locationpermissions"
            http.request.cr.execute(query)
            locations = request.cr.dictfetchall()
            self.regions_list = [location['region'] for location in locations]
            self.biz_hub_list = [location['biz_hub'] for location in locations]
            self.service_centers_list = [location['servicecenter'] for location in locations]
        return self.regions_list, self.biz_hub_list, self.service_centers_list

    
    def getCustomers(self, offset=0, accounttype='Prepaid', queryParam='', limit=0):
        Customers = http.request.env['res.partner']
        http_request = http.request
        self.customers_utils = CustomerUtils(http_request)

        if offset >= 1:
            absolute_offset = (offset * int(QUERY_SETTINGS['LIMIT']))
        else:
            absolute_offset = 0

        if queryParam == '' or queryParam is None:
            if self.hq_user:
                self.key = 'hq'
                query = f"""SELECT 
                                {QuerySelectors.queryselectors_cust}
                            FROM
                                res_partner
                            LEFT OUTER JOIN msms_meter_details ON res_partner.meter_number = msms_meter_details.meter_number
                            WHERE res_partner.accounttype = '{accounttype}'
                            ORDER BY res_partner.surname
                            LIMIT {QUERY_SETTINGS['LIMIT']} OFFSET {absolute_offset};"""
            else:
                query = f"""SELECT 
                                {QuerySelectors.queryselectors_cust}
                            FROM
                                res_partner
                            LEFT OUTER JOIN msms_meter_details ON res_partner.meter_number = msms_meter_details.meter_number
                            WHERE res_partner.accounttype = '{accounttype}' AND res_partner.{self.PERMISSION}
                            ORDER BY res_partner.surname
                            LIMIT {QUERY_SETTINGS['LIMIT']} OFFSET {absolute_offset};"""

            print("Customers query ===>", query)
            http.request.cr.execute(query)
            customers_list = request.cr.dictfetchall()
            return self.customers_utils.makeUrl(Customers, customers_list, accounttype=accounttype)

        else:
            customers_list = Customers.sudo().search([])
            return 'with_param', customers_list

    
    @http.route(['/cms/customers/generic'], website=True,auth='user')
    def get_single_customer_generic(self,accountno):
        try:
            data = self.getSingleCustomer(accountno)
            if data is not None:
                try:
                    response =  data[1]
                    response =  Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
                    response.headers['Cache-Control'] = ASYNC_CUSTOMER_CACHE_CONTROL
                    return response
                except Exception as e:
                    if 'tuple index out of range' in str(e):
                        response = {"status":False}
                        return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
            else:
                response = False
                return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
        except Exception as e:
            data = {'error':str(e)}
            return Response(json.dumps(data, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')
        
    @http.route(['/cms/customers/minified'], website=True,auth='user')
    def get_single_customer_minified(self,accountno,edit_form='0'):
        try:
            http_request = http.request
            self.customers_utils = CustomerUtils(http_request)
            data = self.customers_utils.getMinifiedSingleCustomer(accountno,edit_form)
            if data == False:
                return json.dumps({"status":False,"message":"Something went wrong while fetching record for this customer"})
            in_draft = request.env['customer.drafts'].sudo().search([('accountno', '=', accountno)]).id
                
            if data is not None:
                try:
                    response =  {'status':True,'data':data,'draft':str(in_draft)}
                    response =  Response(json.dumps(response, default=Serializables.jsonSerializer))
                    response.headers['Cache-Control'] = ASYNC_CUSTOMER_CACHE_CONTROL
                    return response
                except Exception as e:
                    if 'tuple index out of range' in str(e):
                        response = {"status":False}
                        return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
            else:
                response = False
                return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
            
        except Exception as e:
            data = {'error':str(e)}
            return Response(json.dumps(data, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')
    
    def getSingleCustomer(self,accountno=None,browse=''):
        http_request = http.request
        self.customers_utils = CustomerUtils(http_request)
        return self.customers_utils.getSingleCustomer(accountno)
        
    def deepSearchCustomers(self,Customers,offset=0,searchparam=None,browse='',rootcmp='',param_type='',paginate='true',field=''):
        http_request = http.request
        self.customers_utils = CustomerUtils(http_request)
        users_lst = self.customers_utils.get_users_list()
        http_request = http.request
        self.permissions_dict = {
                                 'state':http.request.env.user.region,
                                 'buid':http.request.env.user.business_unit,
                                 'servicecenter':http.request.env.user.servicecenter,
                                 'bucode':http.request.env.user.bucode
                                 }
        
        if offset >= 1:
                absolute_offset = (offset * QUERY_SETTINGS['LIMIT'])
        else:
            absolute_offset = 0
        if searchparam !=None and not isinstance(searchparam,dict):
            searchparam = searchparam.strip()
            
        LIMIT = f"LIMIT {QUERY_SETTINGS['LIMIT']} OFFSET {absolute_offset}" if paginate=='true' else ''
        self.WHERE_CLAUSE = f"""WHERE res_partner.{field} ILIKE '%{searchparam}%'""" if field != 'names' else f""" WHERE res_partner.firstname ILIKE '%{searchparam}%' OR
                                                                                                                    res_partner.surname ILIKE '%{searchparam}%' OR
                                                                                                                    res_partner.othernames ILIKE '%{searchparam}%'"""
                
        if 'str' in param_type or 'int' in param_type:
            
            if self.hq_user:
                self.key = 'hq'
                query =     f""" 
                                SELECT 
                                    {QuerySelectors.queryselectors_cust}
                                FROM
                                    res_partner
                                LEFT OUTER JOIN msms_meter_details ON res_partner.meter_number = msms_meter_details.meter_number
                                {self.WHERE_CLAUSE}
                                ORDER BY res_partner.id
                                LIMIT {QUERY_SETTINGS['LIMIT']} OFFSET {absolute_offset};
                            """

            if self.regional_user or self.business_unit_user or self.service_center_user: 
                    
                query =    f""" 
                                SELECT 
                                    {QuerySelectors.queryselectors_cust}
                                FROM
                                    res_partner
                                LEFT OUTER JOIN msms_meter_details ON res_partner.meter_number = msms_meter_details.meter_number
                                {self.WHERE_CLAUSE} AND res_partner.{self.PERMISSION} 
                                ORDER BY res_partner.id
                                LIMIT {QUERY_SETTINGS['LIMIT']} OFFSET {absolute_offset};
                            """
            _logger.info(f"Deep ===> {query}")         
        elif 'dict' in param_type:
            _logger.info(f"Contructing filter query for {searchparam}")
            kwargs = {'users_lst':users_lst,
                        'hq_user':self.hq_user,
                        'rootcmp':rootcmp,
                        'absolute_offset':absolute_offset,
                        'permissions_dict':self.permissions_dict,
                        'service_center_user':self.service_center_user,
                        'business_unit_user':self.business_unit_user,
                        'regional_user':self.regional_user,
                        'QuerySelectors':QuerySelectors,
                        }
            self.constructor = FilterQueryConstructor(searchparam,kwargs,paginate)
            query = self.constructor.construct_query_from_dict()
        _logger.info(f"Advanced filter Query =======> {query}")
        http.request.cr.execute(query)
        customers_list = request.cr.dictfetchall()
        return self.customers_utils.makeUrl(Customers,customers_list,True,browse)
        
    
    @http.route(['/cms/customers/search', '/cms/customers/search/page/<int:page>'], website=True,auth='user')
    def deepsearchcustomers(self,view,page=1,searchparam='',paginate='',offset=0,root_cmp='',field='',**kw):
        self.view_initializer()
        try:
            parsed_q = json.loads(searchparam)
            param_type = str(type(parsed_q))
            searchparam = parsed_q if 'dict' in param_type else searchparam
        except Exception as e:
            param_type = str(type(searchparam))
        
        transients = TransientFields.transient_fields
        defaults = TransientFields.defaults
        field_names = TransientFields.field_names
        defaults = TransientFields.loadUserTransientFields('customerstransientviews') or defaults
        create_perm = Permissions.checkPermissions(http.request.env.user)
        caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
        Customers = http.request.env['res.partner']
        has_field = True if field != '' else False
        try:
            return request.render("cms_ibedc.customers",{"states":states,"self":Customers,"this":self,"regions":self.regions,"business_units":self.business_units,"service_centers":self.service_centers,
                                    "customers":[{}],"component":{'url':'personal_info'},"searchparam":searchparam,"advanced_filters":False,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                                    "appname":"search_results","total_customers":0,'pager': pager,'blockpages':[0],"instance":self,"position":self.http_request.env.user.position,
                                    "create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"field_names":field_names,'transients':transients,"defaults":defaults,"has_field":has_field
                                    })
            

        except Exception as e:
            pager = request.website.pager( url=f'/cms/customers/search',total=0,page=page,step=1,url_args= {'view':view,'searchparam':searchparam})
            return request.render("cms_ibedc.customers",{"states":states,"self":Customers,"this":self,"regions":self.regions,"business_units":self.business_units,"service_centers":self.service_centers,
                                    "customers":[],"component":{'url':'personal_info'},"searchparam":searchparam,"advanced_filters":False,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                                    "appname":"search_results","total_customers":0,'pager': pager,'blockpages':[0],"instance":self,"position":self.http_request.env.user.position,
                                    "create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"field_names":field_names,'transients':transients,"defaults":defaults,"has_field":has_field
                                    })
    
    
    @http.route(['/cms/async_customers/search', '/cms/async_customers/search/page/<int:page>'], website=True,auth='user')
    def async_deepsearchcustomers(self,view,uid,page=1,searchparam='',paginate='',offset=0,field='',**kw):
        # return json.dumps({'status':True,'data':field}, default=Serializables.jsonSerializer) 
        status = checkUid(uid,http.request)
        self.view_initializer()
        try:
            parsed_q = json.loads(searchparam)
            param_type = str(type(parsed_q))
            searchparam = parsed_q if 'dict' in param_type else searchparam
        except Exception as e:
            param_type = str(type(searchparam))
        
        transients = TransientFields.transient_fields
        defaults = TransientFields.defaults
        field_names = TransientFields.field_names
        defaults = TransientFields.loadUserTransientFields('customerstransientviews') or defaults
        create_perm = Permissions.checkPermissions(http.request.env.user)
        caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
        Customers = http.request.env['res.partner']
       
        try:
            this,customers_list,total_searchresults,total_page_results,key,permissions_dict = self.deepSearchCustomers(Customers ,int(offset),
                                                                                                                       searchparam,True,param_type=param_type,
                                                                                                                       paginate=paginate,
                                                                                                                       field=field)
            # if paginate == 'true':
            pager = request.website.pager(url=f'/cms/customers/search', total=total_page_results,page=page,step=PAGINATION_SETTINGS['PER_PAGE'],url_args= {'view':view,'searchparam':searchparam})
            offset = (page - 1) * PAGINATION_SETTINGS['PER_PAGE']
            customers_list = customers_list[offset: offset + PAGINATION_SETTINGS['PER_PAGE']]
            div = total_searchresults / int(QUERY_SETTINGS['LIMIT'])
            if isinstance(div,float) and str(div).split('.')[0]==str(round(div)).split('.')[0]:
                div = div + 1
            blockcount = round(div)
            if total_searchresults < int(QUERY_SETTINGS['LIMIT']):
                blockcount = 1
            blockcount = list(range(blockcount))            
            context = {"states":states,"regions":self.regions,"business_units":self.business_units,"service_centers":self.service_centers,"key":key,"permissions_dict":permissions_dict,
                        "self":this,"customers":customers_list,"component":{'url':'personal_info'},"this":self,"searchparam":str(searchparam).replace('{','').replace('}','').replace("'",'').replace('_',' ').title(),
                        "appname":"deep_search_results","searchfield":field,"total_customers":total_searchresults,'pager': pager,'blockpages':blockcount,"advanced_filters":False,"paginate":True,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                        "create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"field_names":field_names,'transients':transients,"defaults":defaults,"instance":self,
                        
                        }
    
            response =  Response(json.dumps({'status':True,'data':context}, default=Serializables.jsonSerializer)) 
            response.headers['Cache-Control'] = ASYNC_CUSTOMER_CACHE_CONTROL_SHORT
            return response
        
        except Exception as e:
            print(e)
            pager = request.website.pager( url=f'/cms/customers/search',total=0,page=page,step=1,url_args= {'view':view,'searchparam':searchparam})
            context = {"states":states,"self":Customers,"this":self,"regions":self.regions,"business_units":self.business_units,"service_centers":self.service_centers,"error":str(e),
                        "customers":[],"component":{'url':'personal_info'},"searchparam":searchparam,"advanced_filters":False,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                        "appname":"search_results","total_customers":0,'pager': pager,'blockpages':[0],"instance":self,"key":self.key,"permissions_dict":self.permissions_dict,
                        "create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"field_names":field_names,'transients':transients,"defaults":defaults
                        }
            return json.dumps({'status':False,'data':context}, default=Serializables.jsonSerializer) 
    
    @http.route(['/cms/customers', '/cms/customers/page/<int:page>'], website=True,auth='user')
    def customers(self,view,offset=0,page=1,accounttype='Prepaid',**kw):
        # try:
            
            self.view_initializer()
            self.offset = offset
            self.sort_locations()
            transients = TransientFields.transient_fields
            fallback_defaults = TransientFields.defaults
            field_names = TransientFields.field_names
            defaults = TransientFields.loadUserTransientFields('customerstransientviews') or fallback_defaults
            create_perm = Permissions.checkPermissions(http.request.env.user)
            caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
            # print("create perm ===> ", create_perm)
            regions = list(set(self.regions_list)) if self.http_request.env.user.is_headquarters_level_user() else []          
            
            context = {"status":True,
                        "states":states,"regions":regions,"business_units":list(set(self.biz_hub_list)),"service_centers":list(set(self.service_centers_list)),"advanced_filters":False,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                        "component":{'url':'personal_info'},"this":self,'transients':transients,"paginate":True,"has_field":False,"key":self.key,"permissions_dict":self.permissions_dict,"position":self.http_request.env.user.position,
                        "defaults":defaults,"field_names":field_names,"create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"appname":"customers","instance":self
                        }
           
            response =  request.render("cms_ibedc.customers",context)
            return response
                 
    @http.route(['/cms/async_customers', '/cms/async_customers/page/<int:page>'], website=True,auth='user')
    def async_customers(self,view,uid,offset=0,page=1,accounttype='Prepaid',**kw):
        try:
            status = checkUid(uid,http.request)
            self.view_initializer()
            self.offset = offset
            self.sort_locations()
            from datetime import datetime
            now = datetime.now().time() # time object
            this,customers_list,total_customers,total_page_results,key,permissions_dict = self.getCustomers(int(offset),accounttype)
            print(total_customers,total_page_results)
            now = datetime.now().time() # time object
            
            if isinstance(this,str):
                if this == 'with_param':
                    return request.render("cms_ibedc.customers",{"customers":customers_list})
        
            pager = request.website.pager( 
                                        url=f'/cms/customers',
                                        total=total_page_results,
                                        page=page,
                                        step=PAGINATION_SETTINGS['PER_PAGE'],
                                        url_args= {'view':view}
                                        )
            offset = (page - 1) * PAGINATION_SETTINGS['PER_PAGE']
            customers_list = customers_list[offset: offset + PAGINATION_SETTINGS['PER_PAGE']]
            transients = TransientFields.transient_fields
            fallback_defaults = TransientFields.defaults
            field_names = TransientFields.field_names
            defaults = TransientFields.loadUserTransientFields('customerstransientviews') or fallback_defaults
            create_perm = Permissions.checkPermissions(http.request.env.user)
            caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
            div = total_customers / int(QUERY_SETTINGS['LIMIT'] )    
                   
            if isinstance(div,float) and str(div).split('.')[0]==str(round(div)).split('.')[0]:
                div = div + 1
            blockcount = round(div)
            if total_customers < PAGINATION_SETTINGS['PER_PAGE']:
                blockcount = 1
            blockcount = list(range(blockcount))

            def _response():
                context =   {
                                "total_customers":total_customers,'pager': pager,'transients':transients,'blockpages':blockcount,
                                "defaults":defaults,"field_names":field_names,"create_perm":create_perm,
                                "appname":"customers","caad_perm":caad_perm
                            }
                return context

            response = {"template":_response(),"status":True}
            Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
            other_account_type = "Postpaid" if accounttype == "Prepaid" else "Prepaid"
            regions = list(set(self.regions_list)) if self.http_request.env.user.is_headquarters_level_user() else []   #request.env['res.users'].sudo().browse(request.session.uid).region        
            
            context =  {
                            "states":states,"regions":regions,"business_units":list(set(self.biz_hub_list)),"service_centers":list(set(self.service_centers_list)),"advanced_filters":False,
                            "can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                            "self":this,"customers":customers_list,"component":{'url':'personal_info'},"this":self,"response":Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200),
                            "total_customers":total_customers,'pager': pager,'transients':transients,'blockpages':blockcount,"key":self.key,"permissions_dict":self.permissions_dict,"paginate":True,
                            "defaults":defaults,"field_names":field_names,"create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"appname":"customers","instance":self,
                            "pagetitle":accounttype + ' Customers',"accounttype":accounttype,"other_account_type":other_account_type
                           }
           
            response =  Response(json.dumps({'status':True,'data':context}, default=Serializables.jsonSerializer)) 
            response.headers['Cache-Control'] = ASYNC_CUSTOMER_CACHE_CONTROL
            return response

        except Exception as e:
            print(str(e))
            data_object = {"states":states,"regions":list(set(self.regions_list)),"business_units":list(set(self.biz_hub_list)),"service_centers":list(set(self.service_centers_list)),
                            "customers":[],"component":{'url':'personal_info'},"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                            "appname":"customers","total_customers":0,'pager': pager,'blockpages':[0],"error":True,"instance":self,
                            "create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"field_names":field_names,'transients':transients,"defaults":defaults
                            }
            return json.dumps({'status':False,'data':data_object}, default=Serializables.jsonSerializer)

    
    def edit_customer(self,vals_customer, data):
        
        vals_customer['customer_id'] = int(data.get('id'))
        vals_customer['edited_by'] = request.env['res.users'].sudo().browse(request.session.uid).login
        vals_customer['edited_date'] = datetime.datetime.now()
        vals_customer['approved'] = False
        vals_customer['approved_by'] = ''
        vals_customer['status'] = 'Pending'
        vals_customer['is_fresh'] = False
        vals_customer['bhm_aproved'] = False
        vals_customer['auditor_approved'] = False
        
        customer = request.env['customer.editqueue'].sudo().search([('customer_id', '=', int(data.get('id')))])
        in_draft = request.env['customer.drafts'].sudo().search([('customer_id', '=', int(data.get('id')))])
        if in_draft:
            in_draft.write(vals_customer)
        
        vals_customer['is_draft'] = False
        if customer:
            customer.write(vals_customer)
            return 'Customer was updated in queue...'

        return request.env['customer.editqueue'].sudo().create([vals_customer])
        
    @http.route(['/cms/edit_customer/'], website=True,auth='user')
    def edit_customer_view(self,data,**kw):
        data = json.loads(data)
        data['othernames'] = data.pop('othername')
        vals_customer = data
        # print("Backend edit customer data ",vals_customer)
        update_customer = self.edit_customer(vals_customer,data)
        
        response = {"status":True,"data":str(update_customer),"message":"Customer updated data was sent to queue"}  
        return Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8') 
    
    @http.route(['/cms/customers/advancedfiltering/', '/cms/customers/advancedfiltering/page/<int:page>'], website=True,auth='user')
    def advancedfiltering(self,view,q,offset,paginate='true',page=1,**kw):
        self.view_initializer()
        try:
            parsed_q = json.loads(q)
            param_type = str(type(parsed_q))
            searchparam = parsed_q if 'dict' in param_type else q
        except Exception as e:
            pass
        
        # print("Queue====> ", q)
        transients = TransientFields.transient_fields
        defaults = TransientFields.defaults
        field_names = TransientFields.field_names
        defaults = TransientFields.loadUserTransientFields('customerstransientviews') or defaults
        create_perm = Permissions.checkPermissions(http.request.env.user)
        caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
        self.sort_locations()
        Customers = http.request.env['res.partner']
        
        response = request.render("cms_ibedc.customers",{"states":states,"self":Customers,"this":self,"regions":list(set(self.regions_list)),"business_units":list(set(self.biz_hub_list)),"service_centers":list(set(self.service_centers_list)),
                                "customers":[],"component":{'url':'personal_info'},"searchparam":searchparam,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),"position":self.http_request.env.user.position,
                                "appname":"search_results","total_customers":0,"error":False,"instance":self,"advanced_filters":True,"key":self.key,"permissions_dict":self.permissions_dict,
                                "create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"field_names":field_names,'transients':transients,"defaults":defaults
                                })
        response.headers['Cache-Control'] = CACHE_CONTROL
        return response
        
    @http.route(['/cms/customers/async_advancedfiltering/', '/cms/customers/async_advancedfiltering/page/<int:page>'], website=True,auth='user')
    def async_advancedfiltering(self,view,uid,q,offset,rootcmp='',paginate='true',page=1,field='',**kw):
        
        # status = checkUid(uid,http.request)
        self.view_initializer()
        try:
            parsed_q = json.loads(q)
            param_type = str(type(parsed_q))
            searchparam = parsed_q if 'dict' in param_type else q
        except Exception as e:
            pass
        
        transients = TransientFields.transient_fields
        defaults = TransientFields.defaults
        field_names = TransientFields.field_names
        defaults = TransientFields.loadUserTransientFields('customerstransientviews') or defaults
        create_perm = Permissions.checkPermissions(http.request.env.user)
        caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
        self.sort_locations()
        Customers = http.request.env['res.partner']
        try:
            
            this,customers_list,total_searchresults,total_page_results,key,permissions_dict = self.deepSearchCustomers(Customers ,int(offset),searchparam,True,rootcmp=rootcmp,param_type=param_type,paginate=paginate,field=field)
            total_searchresults = len(customers_list)
            pager = request.website.pager( 
                                        url=f'/cms/customers/advancedfiltering',
                                        total=total_searchresults or 0,
                                        page=page,
                                        step=PAGINATION_SETTINGS['PER_PAGE'],
                                        url_args= {'view':view,'q':q}
                                        )
            offset = (page - 1) * PAGINATION_SETTINGS['PER_PAGE']
            customers_list = customers_list[offset: offset + PAGINATION_SETTINGS['PER_PAGE']]
            print("---------------> total results ", total_page_results , QUERY_SETTINGS['LIMIT'])
            div = total_searchresults / int(QUERY_SETTINGS['LIMIT'])
            if isinstance(div,float) and str(div).split('.')[0]==str(round(div)).split('.')[0]:
                div = div + 1
            blockcount = round(div)
            if total_searchresults < int(QUERY_SETTINGS['LIMIT']):
                blockcount = 1
            blockcount = list(range(blockcount))      
            if 'kyc' in searchparam.keys():
                kyc_text = 'Verified' if searchparam['kyc'] == 0 or searchparam['kyc'] == '0'  else 'Unverified'
                searchparam['kyc'] = kyc_text
            searched = str(searchparam).replace(":"," ").replace("{","").replace("}","").replace("_", " ").replace("'","").title()
            other_account_type = "Postpaid" if searchparam['accounttype'] == "Prepaid" else "Prepaid"
            data_object = {"states":states,"regions":list(set(self.regions_list)),"business_units":list(set(self.biz_hub_list)),"service_centers":list(set(self.service_centers_list)),"key":key,"permissions_dict":permissions_dict,
                    "self":this,"customers":customers_list,"component":{'url':'personal_info'},"this":self,"searchparam":str(searchparam).replace('{','').replace('}','').replace("'",'').replace('_',' ').title(),
                    "appname":"search_results","total_customers":total_searchresults,'pager': pager,'blockpages':blockcount,"advanced_filters":True,"paginate":True,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                    "create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"field_names":field_names,'transients':transients,"defaults":defaults,"instance":self,
                    "pagetitle":'Customers Advanced Filtering',"accounttype":[searchparam,f'for {searched}'],"other_account_type":'',
                    }
            response =  Response(json.dumps({'status':True,'data':data_object}, default=Serializables.jsonSerializer))
            response.headers['Cache-Control'] = ASYNC_CUSTOMER_CACHE_CONTROL
            return response

        except Exception as e:
            _logger.info(f"Advanced filtering error  ====> {str(e)}")
            pager = request.website.pager( 
                                        url=f'/cms/customers/search',
                                        total=0,
                                        page=page,
                                        step=1,
                                        url_args= {'view':view,'searchparam':searchparam}
                                        )
            data_object = {"states":states,"self":Customers,"this":self,"regions":list(set(self.regions_list)),"business_units":list(set(self.biz_hub_list)),"service_centers":list(set(self.service_centers_list)),
                            "customers":[],"component":{'url':'personal_info'},"searchparam":searchparam,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                            "appname":"search_results","total_customers":0,'pager': pager,'blockpages':[0],"error":True,"instance":self,
                            "create_perm":create_perm,"caad_perm":caad_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"field_names":field_names,'transients':transients,"defaults":defaults
                            }
            return json.dumps({'status':False,'data':data_object}, default=Serializables.jsonSerializer)
            

class CustomerDetails(http.Controller):
    
    def __init__(self):
        self.abbreviateName = abbreviateName
        
    def processData(data):
        specialChars = ["!","#","$","%","^","&","*","(",")","False","None","None","null","'"]
        for specialChar in specialChars:
            data = data.replace(specialChar, " ")
            if specialChar == "'":
                data = data.replace(specialChar, '"')
        return data
    
    def toLocale(self,value,Float=True):
        try:
            if isinstance(value, int) or isinstance(value, float):
                locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
                if Float:
                    return (locale.format_string('%.2f', float(value), True))
                return (locale.format_string('%.2f', int(value), True))
            else:
                return (locale.format_string('%.2f', 0.00, True))
        except:
            pass
    
    def get_options(self,type):
        options_object_list = []
        models_ids = request.env[type].sudo().search([])
        for model in models_ids:
            if type != 'user.positions':
                new_dict = model.read(fields=['name', 'code'])[0]
            else:
                new_dict = model.read(fields=['name', 'code', 'position_code'])[0]
            options_object_list.append(new_dict)
        return options_object_list
    
    @http.route('/cms/customer_details/',website=True,auth='user') 
    def customers_details(self,component,queryParam,**kwargs):
        caad_roles_list = []
        create_perm = Permissions.checkPermissions(http.request.env.user)
        caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
        caad_roles = request.env['userprocess.hierarchy'].sudo().search([('process_code','=','CAAD')])
        vats = self.get_options('caad.vat')
        for role in caad_roles:
            caad_roles_list.append(role.position_code)
        print('caad roles =========> ', caad_roles_list,vats)
  
        try:
            if queryParam != "":
                http_request = http.request
                self.customer_utils = CustomerUtils(http_request)
                customer_object,customer_data,total_count,count,permission,loc = self.customer_utils.getSingleCustomer(queryParam)
                # print("Customer data ", customer_data)
                
            http.request.cr.execute(f"""select * from respartner_event where accountno = '{queryParam}';""")
            data = http.request.cr.dictfetchone()
            
            self.user_position = http.request.env.user.position 
            refunds = request.env['caad.header'].sudo().search([('accountno','=',queryParam)])
            bucode = request.env['business.units'].sudo().search([('name','ilike',customer_data[0]['buid'])]) #('buid','ilike',customer_data[0]['buid'])
            try:
                customer_data[0]['bucode'] = bucode[0].buid 
                print("Customer BUCODE ======> ", customer_data[0]['bucode'])
            except:
                customer_data[0]['bucode'] = ""
            if data is not None:
                customer_data_e = customer_data 
                edited_fields = data['fields_changed']
                edited_fields = json.loads(edited_fields)
                keys = edited_fields.keys()
                
                for key in keys:
                    customer_data_e[key] = edited_fields[key]
                http.request.cr.execute(f"""delete from respartner_event where accountno = '{customer_data['accountno']}';""")
                response = request.render("cms_ibedc.customer_details",{"ref":{'self':self},"this":self,"component":{'url':component},"refunds":refunds,"position":self.user_position,"caad_roles_list":caad_roles_list,
                                                                        "customerdata":customer_data_e,"vats":vats,"create_perm":create_perm,"caad_perm":caad_perm,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                                                                        "current_user":request.env['res.users'].sudo().browse(request.session.uid).name,},status=301)
                return response
            else:
                response = request.render("cms_ibedc.customer_details",{"ref":{'self':self},"this":self,"component":{'url':component},"refunds":refunds,"position":self.user_position,"caad_roles_list":caad_roles_list,
                                                                    "customerdata":customer_data[0],"vats":vats,"caad_perm":caad_perm,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),"create_perm":create_perm,
                                                                    "current_user":request.env['res.users'].sudo().browse(request.session.uid).name,},status=301)

                response.headers['Cache-Control'] = CACHE_CONTROL
                return response
    
        except Exception as e:
            print("err ====> ", str(e))
            data = [{'id': 0, 'name': '', 'surname': '','error':str(e), 'firstname': '', 'othernames': '', 'mobile': '', 'email': ' ', 'city': '', 'accountno': '', 'statuscode': '', 'accounttype': '', 'bal_cash': '', 'address1': '', 'address2': '', 'applicationdate': '', 'giscoordinate': '', 'guarantorname': '', 'guarantoraddress': '', 'state': '', 'dss_id': '', 'servicecenter': '', 'buid': '', 'title': '', 'gender': '', 'building_description': '', 'lga': '', 'premise_type': '', 'region': '', 'customer_type': '', 'business_type': '', 'lname': '', 'lphone': '', 'injectionstation': '', 'meter_oem': '', 'cin': '', 'is_metered': '', 'feeder_name': '', 'service_band': '', 'upriser_id': '', 'feederid': '', 'ltpoleid': '', 'meter_number': '', 'oldaccountno': '', 'newtariffcode': '', 'outstanding_amnt': '', 'meter_model': '', 'meter_type': '', 'msms_meter_mumber': '', 'meter_manufacturer': '', 'manufacture_year': '', 'meter_rating': '', 'v_rating': '', 'meter_status': '', 'meter_classification': '', 'meter_category': '', 'meter_type_id': '', 'audit_validated_by': '', 'audit_validated_date': '', 'billing_validated_by': '', 'billing_validated_date': '', 'rev_validated_by': '', 'rev_validated_date': '', 'kyc': '', 'bucode': ''}]
            return request.render("cms_ibedc.customer_details",{"error":True,"caad_perm":caad_perm,"vats":vats,"ref":{'self':self},"this":self,"component":{'url':component},"position":http.request.env.user.position,"caad_roles_list":caad_roles_list,"customerdata":data[0],"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),"create_perm":create_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,},status=301)


class Renderer(CustomersView):
    def render_table(self,request,context):
        
        parsed_rows = []
        td_defaults_list = []
        customers = context.get('customers')
        defaults = context.get('defaults')
        transients = context.get('transients')
        field_names = context.get('field_names')
        if len(customers) != 0:
            for customer in customers:
                
                for transient in transients:
                    if transient == 'Name':
                        fullname = str(customer['firstname']) +' ' + str(customer['surname'])+' ' + str(customer['othernames'])
                        abbr = self.abbreviateName(fullname)
                        namecell = get_name_cell()
                        td_defaults_list.append(namecell)
                    else:
                        if transient in defaults:
                            
                            if customer[field_names[transient]] != '' and customer[field_names[transient]] != None:
                                td_defaults = f"""<td>{customer[field_names[transient]]}</td>"""
                            else:
                                td_defaults = f"<td>&#x2022;&#x2022;&#x2022;</td>"
                            td_defaults_list.append(td_defaults)
                        else:
                            if customer[''+field_names[''+transient]] != '' and customer[''+field_names[''+transient]] != None:
                                td_defaults =  f"""<td hidden='1'>{customer[''+field_names[''+transient]]}</td>"""
                            else:
                                 td_defaults = f"""<td hidden='1'>&#x2022;&#x2022;&#x2022;</td>"""
                            td_defaults_list.append(td_defaults)
                            
                if customer['kyc'] == True:
                    td_kyc = """<td> <i style="color:#FF7518!important;" class="material-icons">verified</i></td>"""
                else:
                    td_kyc = """<td > <i style="color:#FF7518!important;" class="material-icons">block</i></td>"""
                
                td_defaults_list.append(customer_table_rows())
                td_defaults_list.append(td_kyc)
                resultant_td_defaults = '\n'.join(td_defaults_list)                
                
                parsed_row = Template(resultant_td_defaults).substitute(accountno=customer.get('accountno'),fullname=fullname,namecell=namecell, abbr=abbr, defaults = resultant_td_defaults)
                parsed_rows.append(parsed_row)
                
            resultant_template = '\n'.join(parsed_rows)
            return Encryption.encryptMessage(resultant_template)



        #     return request.render("cms_ibedc.customers",{
        #                                                 "self":this,"customers":customers_list,"component":{'url':'personal_info'},"this":self,
        #                                                 "total_customers":total_customers,'pager': pager,'transients':transients,'blockpages':blockcount,
        #                                                 "defaults":defaults,"field_names":field_names,"create_perm":create_perm,"current_user":request.env['res.users'].sudo().browse(request.session.uid).name,"appname":"customers"
        #                                                 })