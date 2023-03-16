from datetime import datetime, date
import json
from decimal import *

from .utils import Dashboardutils, convert_date_format, current_week_range, get_previous_n_days, previous_week_range

class Collections(object):
    
    def __init__(self,period,past_date,current_date,key,permissions_dict,hierarchy_order,request):
        
        self.key = key
        self.request = request
        self.permissions_dict = permissions_dict
        self.past_date = '2022-02-28' or past_date
        self.current_date = '2022-02-28' or current_date
        self.period = period
        self.service_center_user = hierarchy_order.get('servicecenter', False) 
        self.business_unit_user = hierarchy_order.get('buid', False) 
        self.regional_user = hierarchy_order.get('state', False) 
        self.hq_user = hierarchy_order.get('hq', False)
        
    def get_collections_query(self):
    
        query_list, headers = self.generateTimelineQuery()
        queries = {}
        default_query = f"""{query_list}"""
        queries['default'] = default_query
        queries['headers'] = headers
        return queries

    def generateTimelineQuery(self):

            current_day = get_previous_n_days(1,shorten= False, get_day_date= False)[0]
            previous_day = get_previous_n_days(2,shorten = False, get_day_date = False)[0]
            self.getpermission_query()
            
            self.AND = f"AND #TABLE_NAME#.{self.PERMISSION}" if self.key !='hq' else ''
    
            query = f"""          
                                    
                                    SELECT CONVERT(date, cus.transdate) AS date, SUM(transamount) AS today_collections,'prepaid' as type
                                    FROM [ecmi_customers_new]
                                    INNER JOIN ecmi_payment_history AS cus ON cus.meterno = [ecmi_customers_new].AccountNo
                                    WHERE CONVERT(date, cus.transdate) = CONVERT(DATE,'{self.current_date}') {self.AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                    GROUP BY CONVERT(date, cus.transdate)


                                    UNION ALL
                                    SELECT CONVERT(date,cus1.paydate) as date,
                                    SUM(payments) as total_collections,'postpaid' as type
                                    FROM [ems_customers_new]
                                    INNER JOIN ems_payments as cus1
                                    ON cus1.accountno = [ems_customers_new].AccountNo
                                    WHERE CONVERT(date,cus1.paydate) = CONVERT(DATE,'{self.current_date}') {self.AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                    GROUP BY CONVERT(date,cus1.paydate)
                        """
            # print(query)
            return query, ['todays_collections','yesterday_collections']

    def getpermission_query(self):
        if self.regional_user :
            self.key = 'state'
            self.PERMISSION = f"""{self.key} = '{self.permissions_dict[self.key].lower()}'"""
            
        if self.business_unit_user:
            self.key = 'buid' 
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
            
        if self.service_center_user:
            self.key = 'servicecenter'
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.buid= '{self.request.user.business_unit}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
           
