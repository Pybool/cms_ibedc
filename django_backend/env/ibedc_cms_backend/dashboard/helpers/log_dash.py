from datetime import datetime, date
import json
from decimal import *
from string import Template
from ..dashboard.recent_payments import RecentPayments
from .dynamic_renderer.recent_payments import ecmi_rows, ems_rows, ecmi_recent_payments_template, ems_recent_payments_template
from ..dashboard.utils import get_days_between_days, split_bracket
from .dashboard_renderer import toLocale, percent_not_available, get_percentages, prepaid_renderer, postpaid_renderer, todays_collections_renderer, feeders_renderer
from ..dashboard.account_types import Accounts
from ..dashboard.online_feeders import OnlineFeeders
from ..dashboard.todays_collection import Collections
from ..dashboard.metering_statistics import MeteringStatistics
from ..dashboard.operation_statistics import OperationsStatistics
from ..dashboard.collection_statistics import CollectionsStatisticsGraph
from operator import itemgetter
from ..parsedate import Datetimeutils
from .customers import CustomerUtils, CustomersView
from odoo import http
from odoo.http import request, Response
from ..utilitymethods.utility import Encryption, Permissions, Serializables, User, abbreviateName
import logging
_logger = logging.getLogger(__name__)

# http://127.0.0.1:8069/cms/dashboard/?view=dashboard&id=gAAAAABjNK5LE9CZD0tPsF3KGSuitXWYyDIFnMHUH_y8ICxEuQ5sJpJpARfY9_4zqLyILT_dAmJLbFsZ2x0wqLESPj_6HH-X3w@@&user=gAAAAABjNK5LHTuG1N-jSvB15wlb7IZ_PkHkmUOIpQn_OJ0GBMubMWXBp5WU8MmJagCohogmyDHAswC0xtCuKjteEkm18--PjgP5gUrpQCJ_MviczKI94Sk@&start_date=2021-10-06&end_date=2022-09-29

class Dashboard(http.Controller):
    
    def __init__(self):
        
        self.toLocale = toLocale
        self.abbreviateName = abbreviateName
        self.percent_not_available = percent_not_available
        self.getpercentages = get_percentages
        self.prepaid_renderer = prepaid_renderer
        self.postpaid_renderer = postpaid_renderer
        self.todays_collections_renderer = todays_collections_renderer
        self.feeders_renderer = feeders_renderer
        
    def getHierarchy(self,request):
        self.service_center_user = request.env.user.is_servicecenter_user() 
        self.business_unit_user = request.env.user.is_businesshub_level_user()
        self.regional_user = request.env.user.is_regional_level_user()
        self.hq_user = request.env.user.is_headquarters_level_user()
        self.permissions_dict = {'state':http.request.env.user.region,'buid':http.request.env.user.business_unit,'servicecenter':http.request.env.user.servicecenter,'bucode':http.request.env.user.bucode}

        if self.regional_user :
            self.key = 'state'
        elif self.business_unit_user:
            self.key = 'buid' 
        elif self.service_center_user:
            self.key = 'servicecenter'
        elif self.hq_user:
            self.key = 'hq'
            
    def fetch_dashboard_metrics(self):
        
        dashboard_data = self.getDashboardData()
        try:
            paymentshistory = self.getRecentPayments(default='ecmi',request=request)[0]
        except Exception as e:
            print("Payments exception ", str(e))
            paymentshistory = []
        
        dashboard_data[0]['recent_payments'] = paymentshistory  
        dashboard_statistics = {"accounts_data":dashboard_data[1],"feeders_data":dashboard_data[2],"ops_data":dashboard_data[3],
                                                                "stats":dashboard_data[0],"create_perm":self.create_perm,"get_pecentages":self.get_percentages,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                                                                "current_user":http.request.env['res.users'].browse(http.request.session.uid).name,'metering_data':dashboard_data[4],
                                                                "today_collections_data":dashboard_data[5] if dashboard_data[5] != None else {}}
        return json.dumps(dashboard_statistics, default=Serializables.jsonSerializer)
        
    def set_default_dashboard(self):
        try:
            data = {}
            metering_data = {}
            ops_data = {}
            data['past_date'] = self.past_date
            data['current_date'] = self.current_date
            data['get_percentages'] = self.get_percentages
            data['period'] = self.period
            
            data['recent_payments'] = []
            data['today_collections'] = 0
            data['yesterday_collections'] = 0
            data['barchart_data'] = []
            ops_data['ev_cust'] = 0
            ops_data['en_cust'] = 0
            ops_data['meter_reading'] = 0
            ops_data['bill_distribution'] = 0
            accounts_default  = {'get_percentages': False, 'prepaid': 0, 'postpaid': 0, 'prev_prepaid_count': 0, 'prev_postpaid_count': 0, 'curr_prepaid_count': 0, 'curr_postpaid_count': 0}
            feeders_default = {'get_percentages': False, 'online_feeders': 0, 'prev_feeders_count': 0, 'curr_feeders_count': 0}
            ops_default = {'get_percentages': True, 'online_feeders': 0, 'prev_feeders_count': 0, 'curr_feeders_count': 0}
            metering_data['doughnut_chart'] = []
            
            return request.render("cms_ibedc.dashboard",{"this":self,"accounts_data":accounts_default,"feeders_data":feeders_default,"ops_data":ops_data,
                                                        "stats":data,"create_perm":self.create_perm,"get_pecentages":'!',"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                                                        "current_user":request.env['res.users'].browse(request.session.uid).name,'metering_data':metering_data,
                                                        "today_collections_data": {}})
        
        except Exception as e:
            print("setdefault error ", e)
            return request.render("cms_ibedc.dashboard",{"this":self,"accounts_data":accounts_default,"feeders_data":feeders_default,"ops_data":ops_data,
                                                        "stats":data,"create_perm":self.create_perm,"get_pecentages":'!',"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                                                        "current_user":request.env['res.users'].browse(request.session.uid).name,'metering_data':metering_data,
                                                        "today_collections_data": {}},lazy=True)

    def __initializer__(self,view,id,user,start_date,end_date):
        period='-1'
        now = datetime.now().time() # time object
        print(f"start initializer {now}")
        self.getHierarchy(request)
        self.abbreviateName = abbreviateName
        self.get_percentages = self.getpercentages(start_date,end_date)
        self.period = period
        self.dt_obj = Datetimeutils(int(period))
        self.past_date = str(start_date)
        self.current_date = str(end_date)
        self.create_perm = Permissions.checkPermissions(http.request.env.user)

        self.uid = Encryption.decryptMessage(id)
        self.login = Encryption.decryptMessage(user)
       
       
    @http.route('/cms/dashboard/',website=True,auth='user')
    def dashboard(self,view,id,user,start_date,end_date,**kw):
        self.__initializer__(view,id,user,start_date,end_date)
        if get_days_between_days(self.past_date,self.current_date) > 366:
            self.set_default_dashboard()
        try:
            userexist = User.isUserExist(self.uid,self.login)
            if userexist:
                try:
                    data = {"this":self,"create_perm":self.create_perm,"get_pecentages":'!',"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                            "current_user":request.env['res.users'].browse(request.session.uid).name}
                    response =  request.render("cms_ibedc.dashboard",data)
                    
                    response.headers['Cache-Control'] = 'max-age=500'
                    return response
                except Exception as e:
                    print("\n\n\n\n\nSilent error"+str(e))
                    try:
                        data = {}
                        metering_data = {}
                        ops_data = {}
                        data['past_date'] = self.past_date
                        data['current_date'] = self.current_date
                        data['get_percentages'] = self.get_percentages
                        data['period'] = self.period
                        
                        data['recent_payments'] = []
                        data['today_collections'] = 0
                        data['yesterday_collections'] = 0
                        data['barchart_data'] = []
                        ops_data['ev_cust'] = 0
                        ops_data['en_cust'] = 0
                        ops_data['meter_reading'] = 0
                        ops_data['bill_distribution'] = 0
                        accounts_default  = {'get_percentages': False, 'prepaid': 0, 'postpaid': 0, 'prev_prepaid_count': 0, 'prev_postpaid_count': 0, 'curr_prepaid_count': 0, 'curr_postpaid_count': 0}
                        feeders_default = {'get_percentages': False, 'online_feeders': 0, 'prev_feeders_count': 0, 'curr_feeders_count': 0}
                        ops_default = {'get_percentages': True, 'online_feeders': 0, 'prev_feeders_count': 0, 'curr_feeders_count': 0}
                        metering_data['doughnut_chart'] = []
                        return request.render("cms_ibedc.dashboard",{"this":self,"accounts_data":accounts_default,"feeders_data":feeders_default,"ops_data":ops_data,
                                                                    "stats":data,"create_perm":self.create_perm,"get_pecentages":'!',"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
                                                                    "current_user":request.env['res.users'].browse(request.session.uid).name,'metering_data':metering_data,})
                    
                    except Exception as e:
                        print("setdefault error ", e)
                        return request.render("cms_ibedc.dashboard",{"this":self,"accounts_data":accounts_default,"feeders_data":feeders_default,"ops_data":ops_data,
                                                                    "stats":data,"create_perm":self.create_perm,"get_pecentages":'!',"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
            
                                                                   "current_user":request.env['res.users'].browse(request.session.uid).name,'metering_data':metering_data,})
            if not userexist:
                return request.render("cms_ibedc.404notfound",{"error":"This profile does not exist on the cms, contact your administrator to create an account for you..."})
        except:
            _logger.error("This user does not exist")
            
                # return request.render("cms_ibedc.404notfound",{})

    def make_headers(self,headers):
        headers = str(headers).replace("'","")
        headers = headers.split("(")[1].split(")")[0]
        return headers
        
    def getDashboardData(self):
        period = '-1'
        accounts = Accounts(self.past_date,self.current_date,self.key, self.permissions_dict,request)
        collections = Collections(self.past_date,self.current_date,self.key, self.permissions_dict,request)
        online_feeders = OnlineFeeders(self.past_date,self.current_date,self.key, self.permissions_dict,request)
        metering_statistics = MeteringStatistics(self.past_date,self.current_date)
        operation_statistics = OperationsStatistics(self.past_date,self.current_date,self.key, self.permissions_dict,request)
        collection_statistics_graph = CollectionsStatisticsGraph(self.past_date,self.current_date, self.key, self.permissions_dict,request)
        
        account_query = accounts.get_account_query()
        collections_query = collections.get_collections_query()
        online_feeders_query = online_feeders.get_online_feeders_query()
        metering_statistics_query = metering_statistics.get_metering_statistics_query()
        collection_statistics_graph_query = collection_statistics_graph.get_collection_statistics_query() 
        operation_statistics_query = operation_statistics.get_ops_statistics_query(self.past_date,self.current_date)
        
        headers = tuple(collections_query['headers'] + collection_statistics_graph_query['headers'])
        headers = str(headers).replace("'","")
        headers = headers.split("(")[1].split(")")[0]
        
        ops_data = {}
        accounts_data = {}
        feeders_data = {}
        metering_data = {}
        today_collections_data = {}
       
        #Get Prepaid and postpaid customers report
        try:
            account_start_time = datetime.now().time()
            _logger.info(f"account_start_time ===> {account_start_time}")
            query = f"""
                        SELECT {self.make_headers(tuple(account_query['headers']))}
                        FROM
                        {account_query['default']}
                    
                    """
            _logger.info(f"Accounts Query {query}")
            http.request.cr.execute(query)
            ret =  request.cr.dictfetchall()[0]
            accounts_data['get_percentages'] = self.get_percentages
            try:
                accounts_data['prepaid'] = int(split_bracket(ret.get('prepaid')))
                accounts_data['postpaid'] = int(split_bracket(ret.get('postpaid')))
            except:
                pass
            
            accounts_data['prev_prepaid_count'] = int(split_bracket(ret.get('prev_prepaid_count')))
            accounts_data['prev_postpaid_count'] = int(split_bracket(ret.get('prev_postpaid_count')))
            try:
                accounts_data['curr_prepaid_count'] = int(split_bracket(ret.get('curr_prepaid_count')))
                accounts_data['curr_postpaid_count'] = int(split_bracket(ret.get('curr_postpaid_count')))
            except:
                accounts_data['curr_prepaid_count'] = 0
                accounts_data['curr_postpaid_count'] = 0 
            account_end_time = datetime.now().time() 
            _logger.info(f"account_end_time ===> {account_end_time}")        
        except Exception as e:
            print("err ",str(e))
            pass
        
        #Get 11KV and 33KV Feeders report
        try:
            feeders_start_time = datetime.now().time() 
            _logger.info(f"feeders_start_time ===> {feeders_start_time}") 
            query = f"""
                        SELECT {self.make_headers(tuple(online_feeders_query['headers']))}
                        FROM
                        {online_feeders_query['default']}
                    """
            http.request.cr.execute(query)
            ret =  request.cr.dictfetchall()[0]
            feeders_data['get_percentages'] = self.get_percentages
            try:
                feeders_data['online_feeders'] = int(split_bracket(ret.get('feeders_11kv'))) + int(split_bracket(ret.get('feeders_33kv')))
            except:
                pass
        
            feeders_data['prev_feeders_count'] = int(split_bracket(ret.get('prev_feeders_count_11kv'))) + int(split_bracket(ret.get('prev_feeders_count_33kv')))
            try:
                feeders_data['curr_feeders_count'] = int(split_bracket(ret.get('curr_feeders_count_11kv'))) + int(split_bracket(ret['curr_feeders_count_33kv']))
            except:
                feeders_data['curr_prepaid_count'] = 0
                feeders_data['curr_postpaid_count'] = 0
            feeders_end_time = datetime.now().time() 
            _logger.info(f"feeders_end_time ===> {feeders_end_time}") 
                            
        except:
            feeders_data['online_feeders'] = 'N/A'
            feeders_data['prev_feeders_count'] = 'N/A'
            feeders_data['curr_feeders_count'] = 'N/A'
            
        #Get Operation Statistics report
        try:
            opsstats_start_time = datetime.now().time() 
            _logger.info(f"opsstats_start_time ===> {opsstats_start_time}") 
            query = f"""
                        SELECT {self.make_headers(tuple(operation_statistics_query['headers']))}
                        FROM
                        {operation_statistics_query['default']}
                    """
            http.request.cr.execute(query)
            ret =  request.cr.dictfetchall()[0]
            ops_data['get_percentages'] = self.get_percentages
            ops_data['ev_cust'] = int(split_bracket(ret.get('ev_cust')))
            ops_data['en_cust'] = int(split_bracket(ret.get('en_cust')))
            ops_data['meter_reading'] = int(split_bracket(ret.get('meter_reading')))
            ops_data['bill_distribution'] = int(split_bracket(ret.get('bill_distribution')))
            
            opsstats_end_time = datetime.now().time() 
            _logger.info(f"opsstats_end_time ===> {opsstats_end_time}") 
            
        except:
            ops_data['ev_cust'] = 0
            ops_data['en_cust'] = 0
            ops_data['meter_reading'] = 0
            ops_data['bill_distribution'] = 0
            # print(ops_data)
            
        #Get Metering Statistics report
        try:
            meter_stats_start_time = datetime.now().time() 
            _logger.info(f"meter_stats_start_time ===> {meter_stats_start_time}") 
            query = f"""
                    SELECT {self.make_headers(tuple(metering_statistics_query['headers']))}
                    FROM
                    {metering_statistics_query['default']}
                """
            http.request.cr.execute(query)
            ret =  request.cr.dictfetchall()[0]
            metering_data['doughnut_chart'] = self.get_doughnut_chart_data(ret)
            meter_stats_end_time = datetime.now().time() 
            _logger.info(f"meter_stats_end_time ===> {meter_stats_end_time}")
        except:
            metering_data['doughnut_chart'] = []
            
        #Get todays collections
        try:
            today_colects_start_time = datetime.now().time() 
            _logger.info(f"today_colects_start_time ===> {today_colects_start_time}")
            query = f"""{collections_query['default']}"""
            _logger.info(f"Today colls Query {query}")
            http.request.cr.execute(query)
            ret =  request.cr.dictfetchall()
            today_collections_data = {}
            today_collections_data['past_date'] = self.past_date
            today_collections_data['current_date'] = self.current_date
            today_collections_data['get_percentages'] = self.get_percentages
            today_collections_data['period'] = self.period
            today_collections_data['today_collections'] = 0 or ret[0].get('today_collections')
            today_collections_data['yesterday_collections'] = 0 or ret[0].get('yesterday_collections')
            today_colects_end_time = datetime.now().time() 
            _logger.info(f"today_colects_end_time ===> {today_colects_end_time}")
        except Exception as e:
            
            today_collections_data['today_collections'] = 0
            today_collections_data['yesterday_collections'] = 0
            
        try:
            
            colections_stats_start_time = datetime.now().time() 
            _logger.info(f"colections_stats_start_time ===> {colections_stats_start_time}")
            query = f"""{collection_statistics_graph_query['default']}"""
            # print(query)
            _logger.info(f"Coolect stats Query {query}")
            http.request.cr.execute(query)
            ret =  request.cr.dictfetchall()
            colections_stats_end_time = datetime.now().time() 
            _logger.info(f"colections_stats_end_time ===> {colections_stats_end_time}")
            # for row in ret:
            #     pass
            data = {}
            data['past_date'] = self.past_date
            data['current_date'] = self.current_date
            data['get_percentages'] = self.get_percentages
            data['period'] = self.period
            # print(ret)
            
            """# Get all dates that were returned with value, as any date without a value is not returned by postgres"""
            
            available_periods = []
            for val in ret: 
                available_periods.append(val.get('period'))
                
            available_periods#.sort()     
            
            """# Search the returned result from query ,if the date is not in query result, create dict with value 0"""
            for idx, period_header in enumerate(collection_statistics_graph_query['headers']):
                if period_header not in available_periods:  
                    ret.append({'period':period_header,'value':0})
                    
            barchart_data = sorted(ret, key=itemgetter('period'))
            colections_statsparse_time = datetime.now().time() 
            _logger.info(f"colections_statsparse_time ===> {colections_statsparse_time}")
            # print(collection_statistics_graph_query['headers'] , barchart_data)
            data['barchart_data'] = barchart_data if isinstance(ret,list) else self.get_bar_chart_data(ret)  
            # print("legit ",data, accounts_data, feeders_data, ops_data, metering_data, today_collections_data)          
            return data, accounts_data, feeders_data, ops_data, metering_data, today_collections_data
        
        except Exception as e:
            print("error ",str(e))
            self.set_default_dashboard()
            data = {}
            data['past_date'] = self.past_date
            data['current_date'] = self.current_date
            data['get_percentages'] = self.get_percentages
            data['period'] = self.period
            data['ev_cust'] = 0
            data['en_cust'] = 0
            data['meter_reading'] = 0
            data['bill_distribution'] = 0
            data['today_collections'] = 0
            data['yesterday_collections'] = 0
            data['barchart_data'] = []
            # print("iillllegit ",data, accounts_data, feeders_data, ops_data, metering_data, today_collections_data)  
            return data, accounts_data, feeders_data, ops_data, metering_data, today_collections_data
            
        
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

        
    def getRecentPayments(self,default='ecmi',request=request):
        
        self.recent_payments = RecentPayments(http,self.key,self.permissions_dict,request)
        if default == 'ecmi':
            payment_list = self.recent_payments.get_ecmi_payments()
        else:
            payment_list = self.recent_payments.get_ems_payments()
            
        megalist = []
        if payment_list:
            for single_dict in payment_list:
                
                single_dict['trans_status'] = str(single_dict['trans_status'])
                single_dict['name'] = str(single_dict['name'])
                if single_dict['name'] == 'None':
                    single_dict['name'] = ''
                if single_dict['trans_status'] == 'None':
                    single_dict['trans_status'] = ''
                megalist.append(single_dict)
                
        return megalist,len(payment_list)
        
    
    def getTodaysCollections(self,date=''):
        now = datetime.now() if date == '' else date
        try:
            dt_string = now.strftime("%d/%m/%y")
            dt_string = dt_string.replace("/","-")
        except:
            dt_string = datetime.strptime(now, '%Y-%m-%d').strftime("%d/%m/%y")
            dt_string = dt_string.replace("/","-")
            
        Paymenthistory = http.request.env['payment.history']
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
    
    @http.route('/cms/dashboard/customer',website=True,auth='user')
    def dashboardCustomer(self,accountno,**kw):
        http_request = http.request
        self.customer_utils = CustomerUtils(http_request)
        singleCustomer,val1,val2,val3,val4,val5 = self.customer_utils.getSingleCustomer(accountno)  #CustomersView.getSingleCustomer(accountno,True)
        if val1 is not None:
            response =  val1[0]
            return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
        else:
            response = False
            return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
        
    @http.route('/cms/dashboard/get_recent_payments',website=True,auth='user')
    def RecentPayment(self,type,**kw):
        
        @property
        def x(self):
            raise NotImplementedError

        self.xml_template = self.render_table(request,type)
        response = {"template":self.xml_template,"status":True}
        return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
    
    

class AsyncDashboard(Dashboard):
    
    @http.route('/cms/get_async_dashboard/',website=True,auth='user')
    def async_dashboard(self,view,id,user,start_date,end_date,**kw):
        super().__initializer__(view,id,user,start_date,end_date)
        data = super().fetch_dashboard_metrics()
        response = {"status":True,'data':data}
        return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)


class Renderer(Dashboard):
    def render_table(self,request,type):
        
        parsed_rows = []
        super().getHierarchy(request)
        data = super().getRecentPayments(default=type,request=request)
        if len(data) == 2:
            for data in data[0]:
                if type == 'ecmi':
                    row = ecmi_rows()
                    parsed_row = Template(row).substitute(name=str(data.get('name')),transref=str(data.get('trans_ref')),
                                            accounttype=str(data.get('accounttype')),meterno=str(data.get('meterno')),
                                            accountno=str(data.get('accountno')),units=str(data.get('units')),trans_date=str(data.get('trans_date')),
                                            trans_amount=str(data.get('trans_amount')),buid=str(data.get('buid')),trans_status=str(data.get('trans_status')),
                                            token=str(data.get('token')),trans_trans_amount=str(data.get('trans_trans_amount')),cost_of_units=str(data.get('cost_of_units')),
                                            abbr_name=self.abbreviateName(str(data.get('name')))
                                            )
                    parsed_rows.append(parsed_row)
                    
                elif type == 'ems':
                    row = ems_rows()
                    parsed_row = Template(row).substitute(payment_id=str(data.get('payment_id')),payment_transaction_id=str(data.get('payment_transaction_id')),
                                            name=str(data.get('name')),receipt_number=str(data.get('receipt_number')),meterno=str(data.get('meterno')),accountno=str(data.get('accountno')),
                                            accounttype=str(data.get('accounttype')),pay_date=str(data.get('pay_date')),payments=str(data.get('payments')),business_unit=str(data.get('business_unit')),
                                            trans_amount=str(data.get('trans_amount')),trans_status=str(data.get('trans_status')),abbr_name=self.abbreviateName(str(data.get('name')))
                                            )
                    parsed_rows.append(parsed_row)
                
            resultant_template = '\n'.join(parsed_rows)
            parent_container = ecmi_recent_payments_template() if type == 'ecmi' else ems_recent_payments_template()
            resultant_template = Template(parent_container).substitute(iteration_loop=resultant_template)
            return resultant_template
