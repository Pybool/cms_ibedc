from datetime import datetime, date
import json
from decimal import *
from .permission import Permission
from .utils import Dashboardutils

class OperationsStatistics(object):
    
    def __init__(self,period,past_date,current_date,key,permissions_dict,hierarchy_order,request):
        
        self.past_date = past_date
        self.current_date = current_date
        self.request = request
        self.key = key
        self.permissions_dict = permissions_dict
        self.period = period
        self.hierarchy_order = hierarchy_order
        
        print("==============================> ", self.key, self.permissions_dict, hierarchy_order)
    
    def get_ops_statistics_query(self,past_date,current_date):
    
        query_list, headers = self.generateTimelineQuery()
        queries = {}
        timeline_query = f"""{query_list[0]}"""
        queries['default'] = timeline_query
        queries['headers'] = headers
        return queries
    
    def generateTimelineQuery(self):
        self.permission = Permission(self.request,self.hierarchy_order,self.key,self.permissions_dict)
        self.get_permission_query = self.permission.get_permission_query
        self.ECMI_AND = f"WHERE #TABLE_NAME#.{self.get_permission_query('ecmi')}" if self.key !='hq' else ''
        self.EMS_AND = f"WHERE #TABLE_NAME#.{self.get_permission_query('ems')}" if self.key !='hq' else ''
        self.DATE_CONJUCTION = f"""AND created_at BETWEEN CONVERT(DATE, '{self.past_date}', 120) AND CONVERT(DATE, '{self.current_date}', 120)""" if self.past_date != self.current_date else ""
      
        self.prepaid_ops_bills = f"""SELECT COUNT(DISTINCT ops_bill_distribution.id) FROM ops_bill_distribution 
                                    INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ops_bill_distribution.account_number 
                                    {self.ECMI_AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                """
        self.prepaid_meter_read = f"""SELECT COUNT(DISTINCT ops_meter_readings.id) FROM ops_meter_readings
                                    INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ops_meter_readings.account_number 
                                    {self.ECMI_AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                """
        self.prepaid_ev_cust = f"""SELECT COUNT(DISTINCT ops_evaluated_customers.id)FROM ops_evaluated_customers 
                                   INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ops_evaluated_customers.account_no 
                                   {self.ECMI_AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                """
        self.prepaid_en_cust = f"""SELECT COUNT(DISTINCT ops_enumerated_customers.id) FROM ops_enumerated_customers 
                                   INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ops_enumerated_customers.account_number 
                                   {self.ECMI_AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                                """
        self.postpaid_ops_bills = f"""SELECT COUNT(DISTINCT ops_bill_distribution.id) FROM ops_bill_distribution 
                                    INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = ops_bill_distribution.account_number 
                                    {self.EMS_AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                """
        self.postpaid_meter_read = f"""SELECT COUNT(DISTINCT ops_meter_readings.id) FROM ops_meter_readings
                                    INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = ops_meter_readings.account_number 
                                    {self.EMS_AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                """
        self.postpaid_ev_cust = f"""SELECT COUNT(DISTINCT ops_evaluated_customers.id)FROM ops_evaluated_customers 
                                   INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = ops_evaluated_customers.account_no 
                                   {self.EMS_AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                """
        self.postpaid_en_cust = f"""SELECT COUNT(DISTINCT ops_enumerated_customers.id) FROM ops_enumerated_customers 
                                   INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = ops_enumerated_customers.account_number 
                                   {self.EMS_AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                                """
        
        print(self.postpaid_en_cust)
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
    
