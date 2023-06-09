from datetime import datetime, date
import json
from decimal import *
from .permission import Permission
from .utils import Dashboardutils, current_week_range, previous_week_range

class OnlineFeeders(object):
    
    def __init__(self,period,past_date,current_date,key,permissions_dict,hierarchy_order,request):
        
        self.key = key
        self.request = request
        self.permissions_dict = permissions_dict
        self.past_date = past_date
        self.current_date = current_date
        self.period = period
        self.hierarchy_order = hierarchy_order
    
    
    def get_online_feeders_query(self):
        self.permission = Permission(self.request,self.hierarchy_order,self.key,self.permissions_dict)
        self.get_permission_query = self.permission.get_permission_query
        self.ECMI_AND = f"WHERE E.{self.get_permission_query('ecmi').replace('#TABLE_NAME#','E')}" if self.key!='hq' else ''
        self.EMS_AND = f"WHERE E.{self.get_permission_query('ems').replace('#TABLE_NAME#','E')}" if self.key!='hq' else ''
        JOINT = 'WHERE' if self.ECMI_AND == '' or self.EMS_AND == '' else 'AND'
        self.DATE_CONJUCTION = f"""{JOINT} F.[Capture DateTime] BETWEEN CONVERT(DATE,'{self.past_date}') AND CONVERT(DATE,'{self.current_date}')""" if self.period == -1 else ''
        default_query = self.generateTimelineQuery()
        queries = {}
        
        queries['default'] = default_query
        return queries
    
    def generateTimelineQuery(self):
        base_query = """SELECT
                        (SELECT COUNT(DISTINCT F.Assetid)
                        FROM [gis_11KV Feeder] AS F
                        INNER JOIN [gis_High_Tension_Pole 11KV] AS H ON H.ht_11kv_parent = F.assetid
                        INNER JOIN gis_distribution_substation_11KV_415 AS D11 ON D11.DSS_11KV_415V_parent = H.Assetid
                        INNER JOIN [ecmi_customers_new] AS E ON E.DSS_ID = D11.assetid #ECMI_AND# #DATE_CONJUCTION#) as prepaid_feeders_11kv,
                        (SELECT COUNT(DISTINCT F.assetid)
                        FROM [gis_33KV Feeder] AS F
                        INNER JOIN [High Tension Pole 33KV] AS H ON H.ht_33kv_parent = F.assetid
                        INNER JOIN gis_distribution_substation_33KV_415 AS D33 ON D33.DSS_33KV_415V_parent = H.Assetid
                        INNER JOIN [ecmi_customers_new] AS E ON E.dss_id = D33.assetid #ECMI_AND# #DATE_CONJUCTION#) as prepaid_feeders_33kv,

                        (SELECT COUNT(DISTINCT F.assetid)
                        FROM [gis_11KV Feeder] AS F
                        INNER JOIN [gis_High_Tension_Pole 11KV] AS H ON H.ht_11kv_parent = F.assetid
                        INNER JOIN gis_distribution_substation_11KV_415 AS D11 ON D11.DSS_11KV_415V_parent = H.Assetid
                        INNER JOIN [ems_customers_new] AS E ON E.DSS_ID = D11.assetid #EMS_AND# #DATE_CONJUCTION#) as postpaid_feeders_11kv,
                        (SELECT COUNT(DISTINCT F.assetid)
                        FROM [gis_33KV Feeder] AS F
                        INNER JOIN [High Tension Pole 33KV] AS H ON H.ht_33kv_parent = F.assetid
                        INNER JOIN gis_distribution_substation_33KV_415 AS D33 ON D33.DSS_33KV_415V_parent = H.Assetid
                        INNER JOIN [ems_customers_new] AS E ON E.dss_id = D33.assetid #EMS_AND# #DATE_CONJUCTION#) as postpaid_feeders_33kv
                        
                        """

        if self.past_date == self.current_date:
           
            query = base_query.replace("#ECMI_AND#",self.ECMI_AND).replace("#EMS_AND#",self.EMS_AND).replace("#DATE_CONJUCTION#",'')
            # print("\n\n\nFeeders query ===> ", query)
            return query
        
        else:
            query =  base_query.replace("#ECMI_AND#",self.ECMI_AND).replace("#EMS_AND#",self.EMS_AND).replace("#DATE_CONJUCTION#",self.DATE_CONJUCTION)
            # print("\n\n\nFeeders query ===> ", query)
            return query
            pass
        
        
                
                
                
