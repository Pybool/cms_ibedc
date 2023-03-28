from datetime import datetime, date
import json
from decimal import *

from .utils import Dashboardutils

class MeteringStatistics(object):
    
    
    def __init__(self,period,past_date,current_date,key,permissions_dict,hierarchy_order,request):
        
        self.key = key
        self.request = request
        self.permissions_dict = permissions_dict
        self.past_date = past_date
        self.current_date = current_date
        self.period = period
        
        self.service_center_user = hierarchy_order.get('servicecenter', False) 
        self.business_unit_user = hierarchy_order.get('buid', False) 
        self.regional_user = hierarchy_order.get('state', False) 
        self.hq_user = hierarchy_order.get('hq', False)
    
    def get_metering_statistics_query(self):
    
        query_list, headers = self.generateTimelineQuery()
        queries = {}
        timeline_query = f"""{query_list}"""
        
        queries['default'] = timeline_query
        queries['headers'] = headers
        return queries
    
    def generateTimelineQuery(self):
        self.getpermission_query()
        
        PERMIT = f"rp.{self.PERMISSION.replace(')','').replace('#TABLE_NAME#','rp')} AND" if self.key != 'hq' else ""
        self.DATE_CONJUCTION = f"""WHERE {PERMIT} p.created_at BETWEEN CONVERT(DATE,'{self.past_date}') AND CONVERT(DATE,'{self.current_date}');""" if self.period==-1 else ''

        query_list =  f"""
                   
                    SELECT
                        SUM(CASE WHEN {PERMIT} p.quantity_installed = '0' THEN 1 ELSE 0 END) as pending_installations,
                        SUM(CASE WHEN {PERMIT} p.quantity_installed = '1' THEN 1 ELSE 0 END) as completed_installations,
                        SUM(CASE WHEN {PERMIT} c.progress='2' THEN 1 ELSE 0 END) as installation_requests
                    FROM
                        msms_customers c
                        JOIN msms_payments p ON c.id = p.customer_id
                        JOIN msms_meter_details_tbl d ON p.meterid = d.id
                        JOIN [ecmi_customers_new] rp ON d.meter_number = rp.MeterNo
                        JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = c.o_account_no
                        {self.DATE_CONJUCTION}

                    
                """
                
        print(query_list)
        return query_list, ['completed_installations','pending_installations','installation_requests']

    def getpermission_query(self):
        if self.regional_user :
            self.key = 'state'
            self.PERMISSION = f"""{self.key} = '{self.permissions_dict[self.key].lower()}'"""
            
        elif self.business_unit_user:
            self.key = 'buid' 
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
            
        elif self.service_center_user:
            self.key = 'servicecenter'
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.buid= '{self.request.user.business_unit}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
           
        else:
            self.key = 'hq'
            self.PERMISSION = ''
        