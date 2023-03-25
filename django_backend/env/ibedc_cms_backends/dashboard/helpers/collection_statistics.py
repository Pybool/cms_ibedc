from datetime import datetime, date
import json
from decimal import *

from .utils import Dashboardutils, convert_date_format, date_range_dates, get_days_between_days, get_month_name, get_months_between_days, get_previous_n_days, start_end_period, weeks_in_month

class CollectionsStatisticsGraph(object):
    
    def __init__(self,period,past_date,current_date,key,permissions_dict,hierarchy_order,request):
        
        self.key = key
        self.period = period
        self.request = request
        self.permissions_dict = permissions_dict
        self.past_date = past_date
        self.current_date = current_date
        
        self.service_center_user = hierarchy_order.get('servicecenter', False) 
        self.business_unit_user = hierarchy_order.get('buid', False) 
        self.regional_user = hierarchy_order.get('state', False) 
        self.hq_user = hierarchy_order.get('hq', False) 
        
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
        self.getpermission_query()
        self.dashboardutils = Dashboardutils(self.period) if int(self.period) <= 0 else Dashboardutils(self.period)
        self.AND = f"AND #TABLE_NAME#.{self.PERMISSION}" if self.key !='hq' else ''
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
                            {self.AND.replace("#TABLE_NAME#","[ecmi_customers_new]")}
                            GROUP BY EP.transdate
                            UNION ALL
                            SELECT paydate AS date, SUM(payments) AS total_collections
                            FROM [ems_customers_new]
                            INNER JOIN ems_payments AS ems ON ems.AccountNo = [ems_customers_new].AccountNo
                            WHERE ems.paydate  BETWEEN CONVERT(DATE,'{self.past_date}') AND CONVERT(DATE,'{self.current_date}')
                            {self.AND.replace("#TABLE_NAME#","[ems_customers_new]")}
                            GROUP BY ems.paydate
                        ) AS data
                        GROUP BY DATEADD(day, DATEDIFF(day, 0, date), 0)
                    """
        # print("\n\n\nCollections stas qury ====> ", query_list)
        return query_list, ['default_graph']
            
        # else:
           
        #     range_dates = tuple(date_range_dates(self.past_date,self.current_date))
        #     number_of_days = len(range_dates)
        #     if number_of_days <= 366 :
        #          headers = []
        #          queries = []
        #          for idx in range(0,len(range_dates)):
        #             comma = '' if len(range_dates)-1 == idx else ',' 
        #             header = 'day_'+str(range_dates[idx])
        #             headers.append(header.replace("-","_")) 
                    
        #          query = f"""SELECT cast(date as text) as period,cast(sum(total_collections) as DOUBLE PRECISION) as value
        #                     FROM

        #                     (
        #                     SELECT TO_DATE(cast(trans_date as text),'YYYY-MM-DD') as date,SUM(trans_amount) as total_collections
        #                     FROM res_partner
        #                     FULL JOIN ecmi_payment_history as EP on EP.meterno = res_partner.accountno
        #                     WHERE TO_DATE(cast(EP.trans_date as text),'YYYY-MM-DD') in {range_dates}
        #                     {self.AND}
        #                     GROUP BY TO_DATE(cast(EP.trans_date as text),'YYYY-MM-DD')

        #                     UNION ALL

        #                     SELECT TO_DATE(cast(pay_date as text),'YYYY-MM-DD') as date,SUM(payments) as total_collections
        #                     FROM res_partner
        #                     FULL JOIN ems_payment_history as ems on ems.accountno = res_partner.accountno
        #                     WHERE pay_date in {range_dates}
        #                     {self.AND}
        #                     GROUP BY TO_DATE(cast(pay_date as text),'YYYY-MM-DD')

        #                     ) as data

        #                     GROUP BY date
        #                 """

        #          return query, list(range_dates)
             
        #     elif number_of_days > 31 and number_of_days <= 366:
                
        #         months_data = {}
        #         headers = []
        #         query_list = []
        #         result = get_months_between_days(self.past_date , self.current_date)
        #         print("\n\n\n\n\nMonth btwn days ",result)
        #         for idx, month in enumerate(result):
        #             start_end = start_end_period('1',month) # Returns start date and end date as a list for a month based on single date in that month
        #             months_data[f'Month {idx}']= {'start_date':str(datetime.strptime(start_end[0],'%Y-%m-%d').strftime('%d-%m-%y')),'end_date':str(datetime.strptime(start_end[1],'%Y-%m-%d').strftime('%d-%m-%y'))}
        #             header = get_month_name(period='month',date_time = datetime.strptime(start_end[0],'%Y-%m-%d'))[:3]
        #             headers.append(header+"_collections")
        #             comma = '' if len(result)-1 == idx else ',' 
        #             query = f"""(SELECT cast(date as text) as period,cast(sum(total_collections) as DOUBLE PRECISION) as value
        #                             FROM

        #                             (
        #                             SELECT TO_DATE(cast(trans_date as text),'YYYY-MM-DD') as date,SUM(trans_amount) as total_collections
        #                             FROM ecmi_payment_history,res_partner
        #                             WHERE TO_DATE(cast(ecmi_payment_history.trans_date as text),'YYYY-MM-DD') 
        #                             BETWEEN TO_DATE('{str(datetime.strptime(start_end[0],'%Y-%m-%d'))}','YYYY-MM-DD') 
        #                             AND TO_DATE('{str(datetime.strptime(start_end[1],'%Y-%m-%d'))}','YYYY-MM-DD')
        #                             AND res_partner.accountno = ecmi_payment_history.meterno
        #                             {self.AND}
        #                             GROUP BY TO_DATE(cast(ecmi_payment_history.trans_date as text),'YYYY-MM-DD')

        #                             UNION ALL

        #                             SELECT TO_DATE(cast(pay_date as text),'YYYY-MM-DD') as date,SUM(payments) as total_collections
        #                             FROM ems_payment_history,res_partner
        #                             WHERE TO_DATE(cast(pay_date as text),'YYYY-MM-DD')
        #                             BETWEEN TO_DATE('{str(datetime.strptime(start_end[0],'%Y-%m-%d'))}','YYYY-MM-DD') 
        #                             AND TO_DATE('{str(datetime.strptime(start_end[1],'%Y-%m-%d'))}','YYYY-MM-DD')
        #                             AND res_partner.accountno = ems_payment_history.accountno
        #                             {self.AND}
        #                             GROUP BY TO_DATE(cast(pay_date as text),'YYYY-MM-DD')

        #                             ) as data

        #                             GROUP BY date
        #                         ) 
        #                         as {header+'_collections'}{comma}
        #                     """
        #             query_list.append(query)
                
        #         resultant_query = '\n'.join(query_list)
        #         return 'SELECT * FROM ' +resultant_query, headers

        #     elif number_of_days > 366:
    
        #         months_data = {}
        #         headers = []
        #         query_list = []
        #         result = get_months_between_days(self.past_date , self.current_date)
        #         for idx, month in enumerate(result):
        #             start_end = start_end_period('1',month) # Returns start date and end date as a list for a month based on single date in that month
        #             months_data[f'Month {idx}']= {'start_date':str(datetime.strptime(start_end[0],'%Y-%m-%d').strftime('%d-%m-%y')),'end_date':str(datetime.strptime(start_end[1],'%Y-%m-%d').strftime('%d-%m-%y'))}
        #             header = get_month_name(period='month',date_time = datetime.strptime(start_end[0],'%Y-%m-%d'))[:3]
        #             headers.append(header+"_collections")
        #             comma = '' if len(result)-1 == idx else ',' 
        #             query = f"""(SELECT sum(payment_history.gross_amount) FROM payment_history WHERE TO_DATE(initiation_date,'DD-MM-YY') BETWEEN TO_DATE('{str(datetime.strptime(start_end[0],'%Y-%m-%d').strftime('%d-%m-%y'))}','DD-MM-YY') AND TO_DATE('{str(datetime.strptime(start_end[1],'%Y-%m-%d').strftime('%d-%m-%y'))}','DD-MM-YY')) as {header+'_collections'}{comma}
        #                     """
        #             query_list.append(query)
                
        #         resultant_query = '\n'.join(query_list)
        #         return resultant_query, headers
            
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
           
