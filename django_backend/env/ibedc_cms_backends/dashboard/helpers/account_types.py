from datetime import datetime, date
from decimal import Decimal

from .utils import Dashboardutils, current_week_range, previous_week_range


class Accounts:
    
    def __init__(self, period, past_date, current_date, key, permissions_dict,hierarchy_order, request):
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
            
    def get_account_query(self):
        self.get_permission_query()
        self.AND = f"WHERE LOWER(E.{self.PERMISSION}" if self.key!='hq' else ''
        JOINT = 'WHERE' if self.AND == '' else 'AND'
        self.DATE_CONJUCTION = f"""{JOINT} [updated_at] BETWEEN CONVERT(DATE, '{self.past_date}', 120) AND CONVERT(DATE, '{self.current_date}', 120)""" if self.period == -1 else ''
        default_query = self.generate_timeline_query()
        # print("\n\n\nAccounts Qury ===> ", default_query)
        return {'default': default_query}
    
    def generate_timeline_query(self):
        if self.past_date == self.current_date:
            if self.key == 'hq':
                return """SELECT
                            (SELECT  count(*) as count FROM [ecmi_customers_new]) AS prepaid_customers,
                            (SELECT  count(*) as count FROM [ems_customers_new]) AS postpaid_customers
                        """
                
            self.get_permission_query()
            return      f"""
                            SELECT
                                (SELECT  count(*) as count FROM [ecmi_customers_new] 
                                WHERE {self.PERMISSION.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                ) AS prepaid_customers,
                                (SELECT  count(*) as count FROM [ems_customers_new] 
                                WHERE {self.PERMISSION.replace("#TABLE_NAME#","[ems_customers_new]")}
                                ) AS postpaid_customers
                            """
       
        else:
            if self.key == 'hq':
                return f"""SELECT
                            (SELECT  count(*) as count FROM [ecmi_customers_new] {self.DATE_CONJUCTION}) AS prepaid_customers,
                            (SELECT  count(*) as count FROM [ems_customers_new] {self.DATE_CONJUCTION}) AS postpaid_customers
                        """
                
            self.get_permission_query()
            return      f"""
                            SELECT
                                (SELECT  count(*) as count FROM [ecmi_customers_new] 
                                WHERE {self.PERMISSION.replace("#TABLE_NAME#","[ecmi_customers_new]")} {self.DATE_CONJUCTION}
                                ) AS prepaid_customers,
                                (SELECT  count(*) as count FROM [ems_customers_new] 
                                WHERE {self.PERMISSION.replace("#TABLE_NAME#","[ems_customers_new]")} {self.DATE_CONJUCTION}
                                ) AS postpaid_customers
                            """
        
    def get_permission_query(self):
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
           
   
