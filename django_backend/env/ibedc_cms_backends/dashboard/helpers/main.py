from .recent_payments import RecentPayments
from .utils import split_bracket
from .account_types import Accounts
from  .collection_statistics import CollectionsStatisticsGraph
from .operation_statistics import OperationsStatistics
from .metering_statistics import MeteringStatistics
from .todays_collection import Collections
from .online_feeders import OnlineFeeders
from datetime import datetime
from connection_executor import dict_fetch_all
from rest_framework.response import Response


class Dashboard(object):
    
    def __init__(self, request):
        self.request = request
        self.view = self.request.GET.get('view')
        self.period = int(self.request.GET.get('period'))
        self.current_date = self.request.GET.get('start_date')
        self.past_date = self.request.GET.get('end_date')
        self.user = self.request.user
        self.permissions_dict = {}
        self.hierarchy_order = {}
        print("Dashboard user ------> ", self.user)
        
        
    def get_hierarchy(self):
        self.key = None
        self.hierarchy_order = {
            'state': self.user.is_level_user('Region'),
            'buid': self.user.is_level_user('Business Unit'),
            'servicecenter': self.user.is_level_user('Service Center'),
            'hq': self.user.is_level_user('Head Quarters'),
        }
        for key, val in self.hierarchy_order.items():
            if val:
                self.key = key
                break
            
        self.permissions_dict = {
            'state': self.user.region,
            'buid': self.user.business_unit,
            'servicecenter': self.user.service_center,
            'bucode': self.user.bucode
        }
        if self.key is None:
            if self.user.permission_hierarchy == 'Head Quarters':
                print({'status':True,"data":self.hierarchy_order})
            return {'status':False,"message":"Your account has no associated hierarchy"}
        return {'status':True}
            
    def fetch_dashboard_metrics(self):
   
        dashboard_data = self.getDashboardData(self.period)        
        try:
            paymentshistory = self.getRecentPayments(default='ecmi', request=self.request)
        except Exception as e:
            print("Recent payment error ===> ",str(e))
            paymentshistory = list()
        
        dashboard_statistics = {
            "accounts_data": dashboard_data[0],
            "recent_payments":paymentshistory
        }
 
        return dashboard_statistics

    def make_headers(self,headers):
        headers = str(headers).replace("'","")
        headers = headers.split("(")[1].split(")")[0]
        return headers
    
    def get_ops_data(self):
        args = {
            "period": self.period,
            "past_date": self.past_date,
            "current_date": self.current_date,
            "key": self.key,
            "permissions_dict": self.permissions_dict,
            "hierarchy_order":self.hierarchy_order,
            "request": self.request,
        }
        operation_statistics = OperationsStatistics(**args)
        operation_statistics_query = operation_statistics.get_ops_statistics_query(self.past_date,self.current_date)
        cols = self.get_collection_ststistics(self.period)
        #################################Get Operation Statistics report###############################################################
        try:
            query = f"""SELECT {operation_statistics_query['default']}"""
            # print("\n\n\nOps Manager qury==> ", query)
            data = dict_fetch_all(query)
            if data:
                return data[0], cols
            return []
            
        except Exception as e:
            print(str(e))
            return {'prepaid_ev_cust': 'N/A', 'prepaid_en_cust': 'N/A', 'prepaid_meter_reading': 'N/A', 'prepaid_bill_distribution': 'N/A',
                        'postpaid_ev_cust': 'N/A', 'postpaid_en_cust': 'N/A', 'postpaid_meter_reading': 'N/A', 'postpaid_bill_distribution': 'N/A'}

    def getDashboardData(self,period):
        
        ops_data = {}
        accounts_data = {}
        recent_payments = {}
        args = {
            "period": period,
            "past_date": self.past_date,
            "current_date": self.current_date,
            "key": self.key,
            "permissions_dict": self.permissions_dict,
            "hierarchy_order":self.hierarchy_order,
            "request": self.request,
        }
        accounts = Accounts(**args)
        
        account_query = accounts.get_account_query()       
        
        #Get Prepaid and postpaid customers report
        
        try:
            query = f"""{account_query['default']}"""
            data = dict_fetch_all(query)
            accounts_data = data 
        except Exception as e:
            print(str(e))
            accounts_data = [{'accounttype': 'Postpaid', 'count': 'N/A'}, {'accounttype': 'Prepaid', 'count': 'N/A'}]
            
        data = {
            'past_date': self.past_date,
            'current_date': self.current_date,
            'period': self.period,
        }
        return accounts_data

    def get_feeders_count(self,request):
        #Get 11KV and 33KV Feeders report
        feeders_data = {}
        try:
            online_feeders = OnlineFeeders(self.period,self.past_date,self.current_date,self.key, self.permissions_dict,self.hierarchy_order,self.request)
            online_feeders_query = online_feeders.get_online_feeders_query() 
            query = f"""{online_feeders_query['default']}"""
            data = dict_fetch_all(query)
            return data
            
                            
        except Exception as e:
            print(str(e))
            feeders_data['online_feeders'] = 'N/A'
            feeders_data['prev_feeders_count'] = 'N/A'
            feeders_data['curr_feeders_count'] = 'N/A'
        
        return [feeders_data]
    
    def get_metering_statistics(self,request):
        #Get Metering Statistics report
        metering_data = {}
        try:
            metering_statistics = MeteringStatistics(self.period,self.past_date,self.current_date,self.key, self.permissions_dict,self.hierarchy_order,self.request)
            metering_statistics_query = metering_statistics.get_metering_statistics_query()
            
            query = f"""{metering_statistics_query['default']}"""
            data = dict_fetch_all(query)
            return data
            
        except Exception as e:
            print(str(e))
            return metering_data

    def get_todays_collections(self):
        try:
            # collections_query = get_collections_query()
            collections = Collections(self.period,self.past_date,self.current_date,self.key, self.permissions_dict,self.hierarchy_order,self.request)
            collections_query = collections.get_collections_query()
            query = collections_query['default']
            data = dict_fetch_all(query)
            return data

            
            
        except Exception as e:
            print(str(e))
            
            
        return {}
    
    def get_collection_ststistics(self, period):
        # collections = Collections(period, self.past_date, self.current_date, self.key, self.permissions_dict, self.request)
        stats_graph = CollectionsStatisticsGraph(period, self.past_date, self.current_date, self.key, self.permissions_dict,self.hierarchy_order, self.request)
        collections_query = stats_graph.get_collection_statistics_query()['default']
        data = dict_fetch_all(collections_query)
        # stats_graph_query = stats_graph.get_collection_statistics_query()
        # headers = tuple(collections_query['headers'] + stats_graph_query['headers'])
        # http.request.cr.execute(str(stats_graph_query['default']))
        # ret =  request.cr.dictfetchall()
        # barchart_data = []
        # existing_periods = {r['period'] for r in ret}
        # missing_periods = [{'period': str(h), 'value': 0} for h in headers if str(h) not in existing_periods]
        # barchart_data = sorted(ret + missing_periods, key=lambda x: str(x['period']))

        # data = {
        #     'past_date': self.past_date,
        #     'current_date': self.current_date,
        #     'get_percentages': self.get_percentages,
        #     'period': period,
        #     'barchart_data': 'barchart_data'
        # }


        return data
   
    def get_bar_chart_data(self,ret):
        ret = ret.copy()
        barchart_data = []
        to_remove = []
        try:
            del ret['todays_collections']
            del ret['yesterday_collections']
        except:
            pass
        for key in ret.keys():
            if "_collections" not in key and "day_" not in key and "default_graph" not in key:
                to_remove.append(key)
        for key in to_remove:
            del ret[key]
        
        for key in ret.keys():
            if "_collections" in key:
                barchart_data.append({
                                    "value":ret.get(key),
                                    "period":key.split('_collections')[0]
                                    
                                    })
            if "day_" in key:
               barchart_data.append({"value":ret.get(key),
                                     "period":key.split('day_')[1].replace("_","-")
                                     })
            
            if "default_graph" in key:
               key_value = ret.get(key).replace('(','').split(',')
               barchart_data.append({"value":key_value[1],
                                     "period":key_value[0]
                                     })
               
        barchart_data = str(barchart_data).replace("'",'"')
        barchart_data = str(barchart_data).replace("()",'0')
        barchart_data = str(barchart_data).replace("(",'')
        barchart_data = str(barchart_data).replace(")",'')
        barchart_data = json.loads(barchart_data)
        
        return barchart_data  
    
    def get_doughnut_chart_data(self,ret):
        ret = ret.copy()
        doughnutchart_data = []
        to_remove = []
       
        for key in ret.keys():
            if "_install" not in key:
                to_remove.append(key)
        for key in to_remove:
            del ret[key]
        
        for key in ret.keys():
            if "_install" in key:
                doughnutchart_data.append({key:ret.get(key)})
        
        doughnutchart_data = str(doughnutchart_data).replace("'",'"')
        doughnutchart_data = str(doughnutchart_data).replace("()",'0')
        doughnutchart_data = str(doughnutchart_data).replace("(",'')
        doughnutchart_data = str(doughnutchart_data).replace(")",'')
        doughnutchart_data = json.loads(doughnutchart_data)
        return doughnutchart_data

    def getTodayPreviousmonth(self,months):
            y = self.dt_obj.months_previous_days_from_now_days(months)
            return self.dt_obj.get_previous_date(y)
     
    def void(self,days,period,q_date):
            
        import pendulum
        date = q_date.split("-")
        year = int(date[0])
        month = int(date[1][1]) if date[0]=='0' else int(date[1])
        day = int(date[2][1]) if date[0]=='0' else int(date[2])
        dt = pendulum.datetime(year, month, day)
        
        if int(period) >= 1: scale = "month"
        if period == '-2': scale = "week"
        if period == '0': return q_date, q_date
        if period == '-1': return q_date, q_date
          
        start = dt.start_of(scale)
        end = dt.end_of(scale)
        return start.to_datetime_string().split(" ")[0], end.to_datetime_string().split(" ")[0]
   
    def getRecentPayments(self,default='ecmi',request=''):
        
        self.recent_payments = RecentPayments(self.key,self.permissions_dict, self.hierarchy_order,request)
        if default == 'ecmi':
            payment_list = self.recent_payments.get_ecmi_payments()
        else:
            payment_list = self.recent_payments.get_ems_payments()
                            
        return payment_list
        
    def getTodaysCollections(self,date=''):
        now = datetime.now() if date == '' else date
        try:
            dt_string = now.strftime("%d/%m/%y")
            dt_string = dt_string.replace("/","-")
        except:
            dt_string = datetime.strptime(now, '%Y-%m-%d').strftime("%d/%m/%y")
            dt_string = dt_string.replace("/","-")
            
        query = f"""    SELECT   
                            sum(payment_history.gross_amount) as today_collections
                        FROM
                            payment_history
                        where payment_history.initiation_date = '{dt_string}'
                        ;
                    """
        http.request.cr.execute(query)
        today_collections = request.cr.dictfetchall()[0]
        if today_collections['today_collections'] is None:
            return {'today_collections': 0.00}

        return today_collections
    
    def calculate_percentage(self,previous,current,yesterday=False):
        
        if self.period == '-1' or self.period == '0' or self.period == '1':
            try:
                getcontext().prec = 4
                self.period = '0' if yesterday else '-1'
                text = {'-1':'vs last week','0':'vs yesterday','1':'vs last month','6':'vs last 6 months','12':'vs last 1 year','48':'vs last 4 years'}
                sign = '+' if current > previous else '-' 
                percentage = float(((Decimal(str(current)) - Decimal(str(previous))) / Decimal(str(previous))) * 100)
                if sign == '-':
                    percentage = float(((Decimal(str(previous)) - Decimal(str(current))) / Decimal(str(previous))) * 100)
                if yesterday == True:
                    pass
                return sign , str(percentage) + "% " + text[self.period]
            except Exception as e:
                return '!', 'N/A'
        else:
            return '!', 'N/A'
        

