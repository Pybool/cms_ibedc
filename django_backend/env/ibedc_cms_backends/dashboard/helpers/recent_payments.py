from datetime import datetime, date
import json
from decimal import *
from connection_executor import dict_fetch_all
import logging
from .permission import Permission
_logger = logging.getLogger(__name__)

class RecentPayments(object):
    
    def __init__(self,key,permissions_dict,hierarchy_order,request):
        self.key = key
        self.request = request
        self.permissions_dict = permissions_dict
        self.hierarchy_order = hierarchy_order
        
        self.permission = Permission(self.request,self.hierarchy_order,self.key,self.permissions_dict)
        self.get_permission_query = self.permission.get_permission_query
        self.ECMI_AND = f"WHERE #TABLE_NAME#.{self.get_permission_query('ecmi')}" if self.key !='hq' else ''
        self.EMS_AND = f"WHERE #TABLE_NAME#.{self.get_permission_query('ems')}" if self.key !='hq' else ''

    def get_ecmi_payments(self):
        
        query = f"""

                    SELECT TOP(50) [ecmi_payment_history].*, ECMIPT.*,ECMI_CUST.*
                    FROM [CMS_IBEDC_DATABASE].[dbo].[ecmi_payment_history]
                    INNER JOIN [ecmi_customers_new] as ECMI_CUST on ECMI_CUST.AccountNo = [ecmi_payment_history].meterno
                    INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.transref = [ecmi_payment_history].transref
                    {self.ECMI_AND.replace("#TABLE_NAME#","ECMI_CUST")}
                    
            
                    """
                #  ORDER BY [ecmi_payment_history].transdate DESC; 
        print(query)  
        return dict_fetch_all(query) 
    
    def get_ems_payments(self):

        query = f"""SELECT TOP(50) [ems_payments].*, EMSPT.*
                    FROM [CMS_IBEDC_DATABASE].[dbo].[ems_payments]
                    INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                    INNER JOIN [ems_customers_new] as EMS_CUST on EMS_CUST.AccountNo = [ems_payment_history].meterno
                    {self.EMS_AND.replace("#TABLE_NAME#","EMS_CUST")}
                    ORDER BY [ems_payments].ProcessedDate DESC;
                    """
        return dict_fetch_all(query) 
