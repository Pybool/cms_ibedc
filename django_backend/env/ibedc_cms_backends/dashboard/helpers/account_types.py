from datetime import datetime, date
from decimal import Decimal
from .utils import Dashboardutils, current_week_range, previous_week_range
from .permission import Permission

class Accounts:
    
    def __init__(self, period, past_date, current_date, key, permissions_dict,hierarchy_order, request):
        self.key = key
        self.request = request
        self.permissions_dict = permissions_dict
        self.past_date = past_date
        self.current_date = current_date
        self.period = period
        self.hierarchy_order = hierarchy_order
         
            
    def get_account_query(self):
        self.permission = Permission(self.request,self.hierarchy_order,self.key,self.permissions_dict)
        self.get_permission_query = self.permission.get_permission_query
        self.EMS_AND = f"WHERE LOWER(E.{self.get_permission_query('ems')}" if self.key!='hq' else ''
        self.ECMI_AND = f"WHERE LOWER(E.{self.get_permission_query('ecmi')}" if self.key!='hq' else ''
        JOINT = 'WHERE' if self.EMS_AND == '' or self.ECMI_AND == '' else 'AND'
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
                
            return      f"""
                            SELECT
                                (SELECT  count(*) as count FROM [ecmi_customers_new] 
                                WHERE {self.get_permission_query('ecmi').replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                ) AS prepaid_customers,
                                (SELECT  count(*) as count FROM [ems_customers_new] 
                                WHERE {self.get_permission_query('ems').replace("#TABLE_NAME#","[ems_customers_new]")}
                                ) AS postpaid_customers
                            """
       
        else:
            if self.key == 'hq':
                return f"""SELECT
                            (SELECT  count(*) as count FROM [ecmi_customers_new] {self.DATE_CONJUCTION}) AS prepaid_customers,
                            (SELECT  count(*) as count FROM [ems_customers_new] {self.DATE_CONJUCTION}) AS postpaid_customers
                        """
                
            return      f"""
                            SELECT
                                (SELECT  count(*) as count FROM [ecmi_customers_new] 
                                WHERE {self.get_permission_query('ecmi').replace("#TABLE_NAME#","[ecmi_customers_new]")} {self.DATE_CONJUCTION}
                                ) AS prepaid_customers,
                                (SELECT  count(*) as count FROM [ems_customers_new] 
                                WHERE {self.get_permission_query('ems').replace("#TABLE_NAME#","[ems_customers_new]")} {self.DATE_CONJUCTION}
                                ) AS postpaid_customers
                            """
        
    