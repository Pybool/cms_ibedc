
import logging
from django.shortcuts import get_object_or_404
_logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import User
from .helpers.main import Dashboard
from config import CACHE_CONTROL
from .helpers.utils import Dashboardutils
from authentication.cms_authenticate import JWTAuthenticationMiddleWare


class AccountTypesView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def get(self,request,**kw):
        self.dashboard_utils = Dashboardutils(request.GET.get('period'))
        
        # if self.dashboard_utils.compare_uid(request):
        self.dashboard = Dashboard(request)
        self.set_hierarchy = self.dashboard.get_hierarchy()
        if self.set_hierarchy['status']:
            data = self.dashboard.fetch_dashboard_metrics()
            feeders =  self.dashboard.get_feeders_count(request)
            response = {"status":True,'data':data,'feeders':feeders}
            response =  Response(response)
            response.headers['Cache-Control'] = CACHE_CONTROL
            return response
        else:
            return Response(self.set_hierarchy)
        # else:
        #     response = {"status":False,"message":"Non matching user id"}
        response =  Response(response)
        return response
    
class OpsmanagerView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def get(self,request,**kw):
        self.dashboard_utils = Dashboardutils(request.GET.get('period'))
        
        # if self.dashboard_utils.compare_uid(request):
        self.dashboard = Dashboard(request)
        self.set_hierarchy = self.dashboard.get_hierarchy()
        if self.set_hierarchy['status']:
            data,cols = self.dashboard.get_ops_data()
            response = {"status":True,'data':{'ops_manager':data,'collection_statistics':cols}}
            response =  Response(response)
            response.headers['Cache-Control'] = CACHE_CONTROL
            return response
        else:
            return Response(self.set_hierarchy)
        # else:
        #     response = {"status":False,"message":"Non matching user id"}
        response =  Response(response)
        return response

class CollectionStatisticsView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def get(self,request,**kw):
        self.dashboard_utils = Dashboardutils(request.GET.get('period'))
        
        if self.dashboard_utils.compare_uid(request):
            self.dashboard = Dashboard(request)
            self.set_hierarchy = self.dashboard.get_hierarchy()
            data = self.dashboard.get_collection_ststistics()
            response = {"status":True,'data':data}
            response =  Response(response)
            response.headers['Cache-Control'] = CACHE_CONTROL
            return response
        else:
            response = {"status":False,"message":"Non matching user id"}
        response =  Response(response)
        return response
    
class TodayCollectionsView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def get(self,request,**kw):
        self.dashboard_utils = Dashboardutils(request.GET.get('period'))
        
        # if self.dashboard_utils.compare_uid(request):
        self.dashboard = Dashboard(request)
        self.set_hierarchy = self.dashboard.get_hierarchy()
        data = self.dashboard.get_todays_collections()
        meter_data =  self.dashboard.get_metering_statistics(request)
        response = {"status":True,'today_cols_data':data,'metering_stats_data':meter_data}
        response =  Response(response)
        response.headers['Cache-Control'] = CACHE_CONTROL
        return response
        # else:
        #     response = {"status":False,"message":"Non matching user id"}
        response =  Response(response)
        return response

class MeteringStatisticsView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def get(self,request,**kw):
        self.dashboard_utils = Dashboardutils(request.GET.get('period'))
        
        # if self.dashboard_utils.compare_uid(request):
        self.dashboard = Dashboard(request)
        self.set_hierarchy = self.dashboard.get_hierarchy()
        data = self.dashboard.get_metering_statistics(request)
        response = {"status":True,'data':data}
        response =  Response(response)
        response.headers['Cache-Control'] = CACHE_CONTROL
        return response
        # else:
        #     response = {"status":False,"message":"Non matching user id"}
        response =  Response(response)
        return response

class FeedersCountView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def get(self,request,**kw):
        self.dashboard_utils = Dashboardutils(request.GET.get('period'))
        
        # if self.dashboard_utils.compare_uid(request):
        self.dashboard = Dashboard(request)
        self.set_hierarchy = self.dashboard.get_hierarchy()
        data = self.dashboard.get_feeders_count(request)
        response = {"status":True,'data':data}
        response =  Response(response)
        response.headers['Cache-Control'] = CACHE_CONTROL
        return response
        # else:
        #     response = {"status":False,"message":"Non matching user id"}
        response =  Response(response)
        return response
    
class DashboardCustomerView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def get(self,request,**kw):
        http_request = http.request
        self.customer_utils = CustomerUtils(http_request)
        singleCustomer,val1,val2,val3,val4,val5 = self.customer_utils.getSingleCustomer(accountno)  #CustomersView.getSingleCustomer(accountno,True)
        if val1 is not None:
            response =  val1[0]
            return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)
        else:
            response = False
            return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)

class RecentPaymentsView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
      
    def RecentPayment(self,type,**kw):
        
        @property
        def x(self):
            raise NotImplementedError
        self.xml_template = self.render_table(request,type)
        response = {"template":self.xml_template,"status":True}
        return Response(json.dumps(response),content_type='text/json;charset=utf-8',status=200)



