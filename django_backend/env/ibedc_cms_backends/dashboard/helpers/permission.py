from location.models import EmsBusinessUnit

def fetch_and_cache_buids():
    data = list(EmsBusinessUnit.objects.filter().values('buid','name','state'))
    return data

def search_for_buid(name,state,lst):
    for d in lst:
        if d["name"].lower() == name.lower() and d["state"].lower() == state.lower():
            return d["buid"]
    return None

class Permission(object):
    
    def __init__(self,request,hierarchy_order,key,permissions_dict):
        self.key = key
        self.request = request
        self.service_center_user = hierarchy_order.get('servicecenter', False) 
        self.business_unit_user = hierarchy_order.get('buid', False) 
        self.regional_user = hierarchy_order.get('state', False) 
        self.hq_user = hierarchy_order.get('hq', False)
        self.permissions_dict = permissions_dict
    
    def get_permission_query(self,type):
        print("Full location chain ===> ", self.request.user.region, self.request.user.business_unit, self.request.user.service_center)
        if self.regional_user :
            self.key = 'state'
            self.PERMISSION = f"""{self.key} = '{self.permissions_dict[self.key].lower()}'"""
            
        if self.business_unit_user or self.service_center_user:
            if self.business_unit_user:
                if type == 'ems':
                    buids = fetch_and_cache_buids()
                    self.buid = search_for_buid(self.permissions_dict.get(self.key, '').lower(), self.request.user.region, buids)
                if type =='ecmi':
                    self.buid = self.permissions_dict.get(self.key, '').lower()
            if self.service_center_user:
                if type == 'ems':
                    buids = fetch_and_cache_buids()
                    self.buid = search_for_buid(self.request.user.business_unit, self.request.user.region, buids)
                if type =='ecmi':
                    self.buid = self.request.user.business_unit
                
        if self.business_unit_user:
            self.key = 'buid' 
            self.PERMISSION = f"{self.key} = '{self.buid}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
            
        if self.service_center_user:
            self.key = 'servicecenter'
            self.PERMISSION = f"{self.key} = '{self.permissions_dict.get(self.key, '').lower()}' AND #TABLE_NAME#.buid= '{self.buid}' AND #TABLE_NAME#.state= '{self.request.user.region}'"
   
        return self.PERMISSION