from datetime import datetime, date
import json
from decimal import *
from .permission import Permission

from .utils import (Dashboardutils, weeks_in_month)


class CollectionsStatisticsGraph(object):
    
    def __init__(self,period,past_date,current_date,key,permissions_dict,hierarchy_order,request):
        
        self.key = key
        self.request = request
        self.permissions_dict = permissions_dict
        self.past_date = past_date
        self.current_date = current_date
        self.period = period
        self.hierarchy_order = hierarchy_order
        
    def get_collection_statistics_query(self) -> dict:
    
        query_list, headers = self.generateTimelineQuery()
        queries = {}
        if isinstance(query_list,list):
            default_query = f"""{query_list[0]}"""
            
        elif isinstance(query_list,str):
            default_query = f"""{query_list}"""
                         
        queries['default'] = default_query
        queries['headers'] = headers
        return queries
    
    def last_365_days_date(self):
        from datetime import datetime, timedelta

        today = datetime.now()
        date_365_days_ago = (today - timedelta(days=365)).strftime('%Y-%m-%d')
        current_date = today.strftime('%Y-%m-%d')
        return date_365_days_ago, current_date
    
    def generateTimelineQuery(self) -> tuple:
        self.permission = Permission(self.request,self.hierarchy_order,self.key,self.permissions_dict)
        self.get_permission_query = self.permission.get_permission_query
        self.dashboardutils = Dashboardutils(self.period) if int(self.period) <= 0 else Dashboardutils(self.period)
        self.EMS_AND = f"AND #TABLE_NAME#.{self.get_permission_query('ems')}" if self.key !='hq' else ''
        self.ECMI_AND = f"AND #TABLE_NAME#.{self.get_permission_query('ecmi')}" if self.key !='hq' else ''
        today = datetime.now()
        if self.past_date == self.current_date and self.current_date == today.strftime('%Y-%m-%d'):
            dates = self.last_365_days_date()
            self.past_date = dates[0]
            self.current_date = dates[1]
    
        if int(self.period) == 1:
            
            weeks_data = {}
            currentMonth = datetime.now().month 
            currentYear = datetime.now().year
            previousMonth = currentMonth - 1
            
            if currentMonth == 1:
                previousMonth = 12
                currentYear =  currentYear - 1
            
            for idx, week in enumerate(weeks_in_month(currentYear, previousMonth)):
                weeks_data[f'Week {idx}']= {'start_date':str(week[0]),'end_date':str(week[1])}
            # print("weks data ===> ", weeks_data)
                

        if int(self.period) == 6:
            
            weeks_data = {}
            currentMonth = datetime.now().month 
            currentYear = datetime.now().year
            previousMonth = currentMonth - 1
            
            if currentMonth == 1:
                previousMonth = 12
                currentYear =  currentYear - 1
            
            for idx, week in enumerate(weeks_in_month(currentYear, previousMonth)):
                weeks_data[f'Week {idx}']= {'start_date':str(week[0]),'end_date':str(week[1])}
                
        # if self.past_date == self.current_date:
        query_list =f"""

                        SELECT CAST(DATEADD(day, DATEDIFF(day, 0, date), 0) AS DATE) AS period, SUM(total_collections) AS value
                        FROM (
                            SELECT EP.transdate AS date, SUM(transamount) AS total_collections
                            FROM [ecmi_customers_new]
                            INNER JOIN ecmi_payment_history AS EP ON EP.meterno = [ecmi_customers_new].AccountNo
                            WHERE EP.transdate BETWEEN CONVERT(DATE,'{self.past_date}') AND CONVERT(DATE,'{self.current_date}')
                            {self.ECMI_AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                            GROUP BY EP.transdate
                            UNION ALL
                            SELECT paydate AS date, SUM(payments) AS total_collections
                            FROM [ems_customers_new]
                            INNER JOIN ems_payments AS ems ON ems.AccountNo = [ems_customers_new].AccountNo
                            WHERE ems.paydate  BETWEEN CONVERT(DATE,'{self.past_date}') AND CONVERT(DATE,'{self.current_date}')
                            {self.EMS_AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                            GROUP BY ems.paydate
                        ) AS data
                        GROUP BY DATEADD(day, DATEDIFF(day, 0, date), 0)
                    """
        # print("\n\n\nCollections stas qury ====> ", query_list)
        return query_list, ['default_graph']
       