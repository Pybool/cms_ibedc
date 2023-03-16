from datetime import datetime, date
import json
from decimal import *
from connection_executor import dict_fetch_all
import logging
_logger = logging.getLogger(__name__)

class RecentPayments(object):
    
    def __init__(self,key,permissions_dict,hierarchy_order,request):
        self.key = key
        self.request = request
        self.permissions_dict = permissions_dict
        self.service_center_user = hierarchy_order.get('servicecenter', False) 
        self.business_unit_user = hierarchy_order.get('buid', False) 
        self.regional_user = hierarchy_order.get('state', False) 
        self.hq_user = hierarchy_order.get('hq', False) 
        self.getpermission_query()
        self.AND = f"WHERE #TABLE_NAME#.{self.PERMISSION}" if self.key !='hq' else ''

    def get_ecmi_payments(self):
        
        query = f"""
                    

                    SELECT TOP(50) [ecmi_payment_history].*, ECMIPT.*,ECMI_CUST.*
                    FROM [CMS_IBEDC_DATABASE].[dbo].[ecmi_payment_history]
                    INNER JOIN [ecmi_customers_new] as ECMI_CUST on ECMI_CUST.AccountNo = [ecmi_payment_history].meterno
                    INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.transref = [ecmi_payment_history].transref
                    {self.AND.replace("#TABLE_NAME#","ECMI_CUST")}
                    
                    
            
                    """
                #  ORDER BY [ecmi_payment_history].transdate; 
        # print(query)  
        return dict_fetch_all(query) 
    
    def get_ems_payments(self):

        query = f"""SELECT TOP(100) [ems_payments].*, EMSPT.*
                    FROM [CMS_IBEDC_DATABASE].[dbo].[ems_payments]
                    INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                    INNER JOIN [ems_customers_new] as EMS_CUST on EMS_CUST.AccountNo = [ems_payment_history].meterno
                    {self.AND.replace("#TABLE_NAME#","EMS_CUST")}
                    ORDER BY [ems_payments].ProcessedDate DESC;
                    """
        return dict_fetch_all(query) 
    

    def getpermission_query(self):
        print("Full location chain ===> ", self.request.user.region, self.request.user.business_unit, self.request.user.service_center)
        if self.regional_user :
            self.key = 'state'
            self.PERMISSION = f"""{self.key} = '{self.permissions_dict[self.key].lower()}'"""
            
        if self.business_unit_user:
            self.key = 'buid' 
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
            
        if self.service_center_user:
            self.key = 'servicecenter'
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.buid= '{self.request.user.business_unit}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
           
