import json
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import User
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
from connection_executor import dict_fetch_all
from .raw_queries import *
from config import CACHE_CONTROL


class SingleCustomerAssets(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self, request):
        accountno = request.GET.get('accountno')
        accounttype = request.GET.get('accounttype')
        tables = {'prepaid':'ecmi_customers_new','postpaid':'ems_customers_new'}
        query =  SINGLE_CUSTOMER_ASSETS_INFO_11KV\
                    .replace("#AccountNo#",accountno)\
                    .replace("#CUSTOMER_TABLE#",tables[accounttype])\

        assets = dict_fetch_all(query)#Emsassets.objects.filter(accountno__iexact=accountno).all().order_by('id')[:10]
        if assets:
            response = {"status": True, "data": assets}
        else:
            query =  SINGLE_CUSTOMER_ASSETS_INFO_33KV\
                    .replace("#AccountNo#",accountno)\
                    .replace("#CUSTOMER_TABLE#",tables[accounttype])\

            assets = dict_fetch_all(query)
            if assets:
                response = {"status": True, "data": assets}
            else:
                response = {"status": False, "message": "No customer assets found with the provided account number."}
        return Response(response)
    
    
class FetchGisAssetInfo(APIView):  
    # authentication_classes = [JWTAuthenticationMiddleWare]  
    # http://192.168.15.160:8069/cms/gis/getasset_info?dss_owner=Kemta&asset_type=dss&feeder_type=&cuid=8
    # http://127.0.0.1:8000/api/v1/cms/gis/getasset_info?dss_owner=&asset_type=dss_owner&feeder_type=
    def get(self,request,**kw):
        try:
            dss_owner = request.GET.get('dss_owner')
            asset_type = request.GET.get('asset_type')
            feeder_type= request.GET.get('feeder_type','')
            
            data_type = ''
            if asset_type == 'dss':
                query = FETCH_GIS_ASSETS_INFO.replace('#dss_owner#',dss_owner)
                data_type = 'dss_name'
            elif asset_type == 'feeders':
                if feeder_type == '11kv':
                    query = """ select f11kv_feeder_name as feeders,assetid from gis_ibedc_11kv_feeder
                            """
                    data_type = '11kv'
                else:
                    query = """ select f33kv_feeder_name as feeders,assetid from gis_ibedc_33kv_feeder
                            """
                    data_type = '33kv'
            elif asset_type == 'dss_owner':
                query = FETCH_GIS_ASSETS_INFO_DSS_OWNER
            
            assets = dict_fetch_all(query)
            data = {"status":True,"data":assets,"type":data_type}
            response =  Response(data)
            return response 
        except Exception as e:
            response = {'status':False,'message': str(e)}
            return Response(response)
        
class FetchFeederView(APIView):
    def get(self,request,**kw):
        try:
            assetid = request.GET.get('assetid')
            query = FETCH_GIS_FEEDER_INFO.replace('#assetid#',assetid)
            feeders = dict_fetch_all(query)
            data = {"status":True,"data":feeders}
            response =  Response(data)
            return response 
        except Exception as e:
            response = {'status':False,'message': str(e)}
            return Response(response)
        

class FetchISSView(APIView):
    def get(self,request,**kw):
        try:
            dss_id = request.GET.get('dss_id')
            query = FETCH_ISS_INFO.replace('#dss_id#',dss_id)
            iss = dict_fetch_all(query)
            data = {"status":True,"data":iss}
            response =  Response(data)
            return response 
        except Exception as e:
            response = {'status':False,'message': str(e)}
            response = Response(response)
            response.headers['Cache-Control'] = CACHE_CONTROL
            return response