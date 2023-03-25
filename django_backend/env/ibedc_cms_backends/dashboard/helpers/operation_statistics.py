from datetime import datetime, date
import json
from decimal import *

from .utils import Dashboardutils

class OperationsStatistics(object):
    
    def __init__(self,period,past_date,current_date,key,permissions_dict,hierarchy_order,request):
        
        self.past_date = past_date
        self.current_date = current_date
        self.request = request
        self.key = key
        self.permissions_dict = permissions_dict
        self.period = period
        self.service_center_user = hierarchy_order.get('servicecenter', False) 
        self.business_unit_user = hierarchy_order.get('buid', False) 
        self.regional_user = hierarchy_order.get('state', False) 
        self.hq_user = hierarchy_order.get('hq', False)
        
        print("==============================> ", self.key, self.permissions_dict, hierarchy_order)
    
    def get_ops_statistics_query(self,past_date,current_date):
    
        query_list, headers = self.generateTimelineQuery()
        queries = {}
        timeline_query = f"""{query_list[0]}"""
        queries['default'] = timeline_query
        queries['headers'] = headers
        return queries
    
    def generateTimelineQuery(self):
        self.getpermission_query()
        self.AND = f"WHERE #TABLE_NAME#.{self.PERMISSION}" if self.key !='hq' else ''
        self.DATE_CONJUCTION = f"""AND created_at BETWEEN CONVERT(DATE, '{self.past_date}', 120) AND CONVERT(DATE, '{self.current_date}', 120)""" if self.past_date != self.current_date else ""
      
        self.prepaid_ops_bills = f"""SELECT COUNT(DISTINCT ops_bill_distribution.id) FROM ops_bill_distribution 
                                    INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ops_bill_distribution.account_number 
                                    {self.AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                """
        self.prepaid_meter_read = f"""SELECT COUNT(DISTINCT ops_meter_readings.id) FROM ops_meter_readings
                                    INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ops_meter_readings.account_number 
                                    {self.AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                """
        self.prepaid_ev_cust = f"""SELECT COUNT(DISTINCT ops_evaluated_customers.id)FROM ops_evaluated_customers 
                                   INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ops_evaluated_customers.account_no 
                                   {self.AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                """
        self.prepaid_en_cust = f"""SELECT COUNT(DISTINCT ops_enumerated_customers.id) FROM ops_enumerated_customers 
                                   INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ops_enumerated_customers.account_number 
                                   {self.AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                """
        self.postpaid_ops_bills = f"""SELECT COUNT(DISTINCT ops_bill_distribution.id) FROM ops_bill_distribution 
                                    INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = ops_bill_distribution.account_number 
                                    {self.AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                """
        self.postpaid_meter_read = f"""SELECT COUNT(DISTINCT ops_meter_readings.id) FROM ops_meter_readings
                                    INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = ops_meter_readings.account_number 
                                    {self.AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                """
        self.postpaid_ev_cust = f"""SELECT COUNT(DISTINCT ops_evaluated_customers.id)FROM ops_evaluated_customers 
                                   INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = ops_evaluated_customers.account_no 
                                   {self.AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                """
        self.postpaid_en_cust = f"""SELECT COUNT(DISTINCT ops_enumerated_customers.id) FROM ops_enumerated_customers 
                                   INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = ops_enumerated_customers.account_number 
                                   {self.AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                """
        

        query_list = [
                f"""
                ( {self.prepaid_meter_read} {self.DATE_CONJUCTION}) as prepaid_meter_reading,
                ( {self.prepaid_ops_bills} {self.DATE_CONJUCTION} ) as prepaid_bill_distribution,
                ( {self.prepaid_ev_cust } {self.DATE_CONJUCTION}) AS prepaid_ev_cust,
                ( {self.prepaid_en_cust } {self.DATE_CONJUCTION}) AS prepaid_en_cust,
                ( {self.postpaid_meter_read} {self.DATE_CONJUCTION}) as postpaid_meter_reading,
                ( {self.postpaid_ops_bills} {self.DATE_CONJUCTION} ) as postpaid_bill_distribution,
                ( {self.postpaid_ev_cust } {self.DATE_CONJUCTION}) AS postpaid_ev_cust,
                ( {self.postpaid_en_cust } {self.DATE_CONJUCTION}) AS postpaid_en_cust
                """
                ]
  
        return query_list, ['prepaid_meter_reading','prepaid_bill_distribution','prepaid_ev_cust','prepaid_en_cust',
                            'postpaid_meter_reading','postpaid_bill_distribution','postpaid_ev_cust','postpaid_en_cust']
    
    def getpermission_query(self):
        print("Full location chain ===> ", self.request.user.region, self.request.user.business_unit, self.request.user.service_center)
        if self.regional_user :
            self.key = 'state'
            self.PERMISSION = f"""{self.key} = '{self.permissions_dict[self.key].lower()}'"""
            
        elif self.business_unit_user:
            self.key = 'buid' 
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
            print("SELF>PERMISSION ", self.PERMISSION)
            
        elif self.service_center_user:
            self.key = 'servicecenter'
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.buid= '{self.request.user.business_unit}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
           

            
            
            
# from datetime import datetime, date
# import json
# from decimal import *
# from .utils import Dashboardutils


# class OperationsStatistics:
    
#     def __init__(self, period, past_date, current_date, key, permissions_dict,hierarchy_order, request):
#         self.past_date = past_date
#         self.current_date = current_date
#         self.key = key
#         self.permissions_dict = permissions_dict
#         self.period = period
#         self.service_center_user = hierarchy_order.get('servicecenter', False) 
#         self.business_unit_user = hierarchy_order.get('buid', False) 
#         self.regional_user = hierarchy_order.get('state', False) 
#         self.hq_user = hierarchy_order.get('hq', False)
    
#     def get_ops_statistics_query(self, past_date, current_date):
#         query_list, headers = self.generate_timeline_query()
#         queries = {'default': query_list[0], 'headers': headers}
#         return queries
    
#     def generate_timeline_query(self):
#         self.get_permission_query()
#         self.and_clause = ''
#         if self.key != 'hq':
#             self.and_clause = f"WHERE LOWER(res_partner.{self.permission})"

#         date_clause = ''
#         if self.past_date != self.current_date:
#             date_clause = f"""AND created_at::date BETWEEN TO_DATE('{self.past_date}', 'YYYY-MM-DD') AND TO_DATE('{self.current_date}', 'YYYY-MM-DD')"""

#         self.ops_bills = f"""
#             SELECT COUNT(DISTINCT ops_bill_distribution.id)
#             FROM ops_bill_distribution
#             LEFT OUTER JOIN res_partner ON res_partner.accountno = ops_bill_distribution.account_number
#             {self.and_clause}
#         """
#         self.meter_read = f"""
#             SELECT COUNT(DISTINCT ops_meter_reading.id)
#             FROM ops_meter_reading
#             LEFT OUTER JOIN res_partner ON res_partner.accountno = ops_meter_reading.account_number
#             {self.and_clause}
#         """
#         self.ev_cust = f"""
#             SELECT COUNT(DISTINCT ops_evaluated_customers.id)
#             FROM ops_evaluated_customers
#             LEFT OUTER JOIN res_partner ON res_partner.accountno = ops_evaluated_customers.accountno
#             {self.and_clause}
#         """
#         self.en_cust = f"""
#             SELECT COUNT(DISTINCT ops_enumerated_customers.id)
#             FROM ops_enumerated_customers
#             LEFT OUTER JOIN res_partner ON res_partner.accountno = ops_enumerated_customers.account_number
#             {self.and_clause}
#         """
        
#         query_list = [
#             f"""({self.meter_read} {date_clause}) AS meter_reading""",
#             f"""({self.ops_bills} {date_clause}) AS bill_distribution""",
#             f"""({self.ev_cust} {date_clause}) AS ev_cust""",
#             f"""({self.en_cust} {date_clause}) AS en_cust"""
#         ]
  
#         return query_list, ['meter_reading', 'bill_distribution', 'ev_cust', 'en_cust']
    
#     def get_permission_query(self):
#         print(self.key)
#         if self.regional_user:
#             self.key = 'state'
#             self.permission = f"""{self.key}) = '{self.permissions_dict[self.key].lower()}'"""
            
#         if self.business_unit_user:
#             self.key = 'buid' 
#             self.permission = f"""{self.key}) IN ('{self.permissions_dict[self.key].lower()}','{self.permissions_dict["bucode"]}')"""
            
#         if self.service_center_user:
#             self.key = 'servicecenter'
#             self.permission = f"""{self.key}) = '{self.permissions_dict[self.key].lower()}'"""
