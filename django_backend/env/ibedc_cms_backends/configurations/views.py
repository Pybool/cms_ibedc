import json, uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User, UserPositions
from .models import UserProcessHierarchy, AccountType,BuildingDescription, CustomerCategory,CustomerType,PremiseType,SupplyType,ServiceBand, CaadVat
from authentication.helpers.permissions import Permissions
from authentication.cms_authenticate import ( JWTAuthenticationMiddleWare )
model_map = {
                'accounttype': AccountType,
                'building_description': BuildingDescription,
                'customer_category': CustomerCategory,
                'customer_type': CustomerType,
                'premise_type': PremiseType,
                'supply_type': SupplyType,
                'service_band': ServiceBand,
                'caad_vat':CaadVat,
                'user_positions':UserPositions
            }

def build_data(data,type=''):
        
    data_object_list = []
    for item in data:
        data_object = {}
        if isinstance(item,str):
            data_object['name'] = item
            data_object['code'] = str(uuid.uuid4())
            if type == 'user.positions':
                data_object['position_code'] = item.split('(')[1].split(')')[0]
        elif isinstance(item,dict):
            data_object['precedence'] = item.get('precedence')
            data_object['process_code'] = item.get('process_code')
        data_object_list.append(data_object)
    return data_object_list

def convert_record_to_dict(self,records):
        options_object_list = []
        models_ids = records
        for model in models_ids:
            new_dict = model.read(fields=['position_code'])[0]
            options_object_list.append(new_dict)
        return options_object_list
    
def get_options(type):
    
    if type != 'user_positions':
        options_object_list =  model_map[type].objects.filter().values('name', 'code')
    else:
        options_object_list = model_map[type].objects.filter().values('name', 'code', 'position_code')
    return options_object_list
    
class SettingsView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        create_perm = Permissions.checkPermissions(request.user,'CUST-CU')
        caad_perm = Permissions.checkPermissions(request.user,'CAAD')
        
        try:
            user_positions = UserPositions.objects.all().values()
            cust_cu_roles = UserProcessHierarchy.objects.filter(process_code='CUST-CU').values()
            cust_kyc_roles = UserProcessHierarchy.objects.filter(process_code='CUST-KYC').values()
            biz_hub_ops_roles = UserProcessHierarchy.objects.filter(process_code='BHM-OPC').values()
            caad_roles = UserProcessHierarchy.objects.filter(process_code='CAAD').values()
            processes = UserProcessHierarchy.get_processes()
            print({
                'cust_cu_roles': cust_cu_roles,
                'cust_kyc_roles': cust_kyc_roles,
                'biz_hub_ops_roles': biz_hub_ops_roles,
                'caad_roles': caad_roles,
                'processes': processes,
                'user_positions': user_positions,
                'create_perm': create_perm,
                'caad_perm': caad_perm,
                'current_user': User.objects.get(id=request.user.id).name
            })
            return Response({
                'cust_cu_roles': cust_cu_roles,
                'cust_kyc_roles': cust_kyc_roles,
                'biz_hub_ops_roles': biz_hub_ops_roles,
                'caad_roles': caad_roles,
                'processes': processes,
                'user_positions': user_positions,
                'create_perm': create_perm,
                'caad_perm': caad_perm,
                'current_user': User.objects.get(id=request.user.id).name
            })
            
        except Exception as e:
            print(str(e))
            return Response({
                'create_perm': create_perm,
                'caad_perm': caad_perm,
                'current_user': User.objects.get(id=request.user.id).name
            })
            
    # @http.route('/cms/settings/create_options/',website=True,auth='none')
class CreateOptions(APIView):
    def post(self, request, **kw):
        try:
            print(request.data)
            print(request.GET)
            
            option_type = request.data.get('value')
            if isinstance(option_type,dict):
                buffer = option_type.get('position_code')
                option_type = option_type.get('value')
            options = request.data.get('data')
            options = build_data(options, option_type)
            
            model_class = model_map.get(option_type)

            # Create hierarchy if applicable
            if len(options) == 2 and 'precedence' in options[1]:
                hierarchy_data = options[1]
                options[0]['position_code'] = buffer
                # print("Position code ===> ", buffer)
                hierarchy_data['position_code'] = buffer
                hierarchy_data['precedence'] = int(hierarchy_data['precedence'])
                print('To create ===> ',options[0])
                created_option = model_class.objects.create(**options[0])
                if created_option.id:
                    UserProcessHierarchy.objects.create(**hierarchy_data)
            
            else:
                # Create options
                created_options = []
                print("Options====> ", options)
                for option in options:
                    created_option = model_class.objects.create(**option)
                    created_options.append(created_option)
                    print("created option:", created_option)

            response = {"status": True, "message": "New options were created..."}
            return Response(response)
        except Exception as e:
            response = {"status": False, "message": f"Could not create options... {str(e)}"}
            return Response(response)


    
    # @http.route('/cms/settings/read_options/',website=True,auth='user',csrf=False)
class ReadSettingsView(APIView):
    def get(self,request,**kw):
        try:
            type = request.GET.get('type')
            options = get_options(type)
            data = {"status":True,"options":options}  if len(options) > 0 else {"status":False,"options":[]}
            response =  Response(data)
            response.headers['Cache-Control'] = 'no-cache'#SETTINGS_CACHE_CONTROL
            return response 
        except Exception as e:
            print("::::::",str(e))
            # return request.render("cms_ibedc.settings_page",{"error":str(e)}) 
        
    # @http.route('/cms/settings/update_options/',website=True,auth='user')
class UpdateSettingsView(APIView):
    def put(self,request,**kw):
        try:
            print("==========> xx",request.data)
            option_type = request.data.get('value')
            data = request.data.get('data')
            model_class = model_map.get(option_type)
            ModelClass = model_class.objects
            records = data
            for record in records:
                # filter the queryset based on the 'code' field
                qs = ModelClass.filter(code=record.get('code'))
                # update the fields of the queryset using the record values
                msg = qs.update(**record)

                print(msg)
            if msg == True:
                response = {"status":True,"message":"Update was successful"}
            else:
                response = {"status":False,"message":"Update was not successful"}
            return Response(response)
        except Exception as e:
            return Response({"status":False,"message":"Update was not successful"})
        
    # @http.route('/cms/settings/delete_options/',website=True,auth='user',csrf=False)
class DeleteSettingsView(APIView):
    def delete(self,request,**kw):
        try:
            option_type = request.GET.get('type')
            code = request.GET.get('code')
            model_class = model_map.get(option_type)
            ModelClass = model_class.objects
            queryset = ModelClass.get(code=code)
            queryset.delete()

            response = {"status":True,"message":"Option was deleted..."}
            response =  Response(response)
            response.headers['Cache-Control'] = 'no-cache'
            return response  
        except Exception as e:
            print
            response = {"status":False,"message":"Option was not deleted..."}
            return Response(response)
    
    # @http.route('/cms/settings/update_role_hierarchy/',website=True,auth='none')
class UpdateHierarchyView(APIView):
    def put(self,request,**kw):
        # try:
            data = json.loads(request.GET.get('data'))
            process_code = request.GET.get('process_code')
            for d in data:
                d['precedence'] = int(d['precedence'])
                print(d,process_code)
                exist = UserProcessHierarchy.objects.filter(position_code=d["position_code"], process_code=process_code).exists()
                print("Exist ",exist)
                if not exist:
                    print("here")
                    UserProcessHierarchy.objects.create(**d)
                    response = {"status":True,"message":"New Roles Were Assigned Successfully..."}
                else:
                    UserProcessHierarchy.objects.filter(position_code=d["position_code"], process_code=process_code).update(**d)
                    response = {"status":True,"message":"Roles Were updated Successfully..."}
            
            return Response(response) 
        # except Exception as e:
        #     print(str(e))
            # return request.render("cms_ibedc.settings_page",{{"error":str(e)}})  
    
    # @http.route('/cms/settings/delete_role_hierarchy/',website=True,auth='none')
    def delete_role_hierarchy_view(self,position_code,process_code,**kw):
        try:
            UserProcessHierarchy.objects.search([('position_code' , '=', position_code),('process_code','=',f'{process_code}')]).unlink()
            response = {"status":True,"message":"Role was deleted..."}
            return json.dumps(response, default=Serializables.jsonSerializer) 
        except Exception as e:
            return request.render("cms_ibedc.settings_page",{"error":str(e)})
        

class Options(APIView):
    def get(self,request,**kw):
        return ReadSettingsView.get(ReadSettingsView,request)
    
    def put(self,request):            
        return self.update_settings_options_view(request,request.GET.get('data'))
    
    def delete(self,request):
        return DeleteSettingsView.delete(DeleteSettingsView,request)   
    
