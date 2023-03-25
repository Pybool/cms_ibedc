from .models import *
from django.db import transaction

class AuditLogView(object):
    
    def __init__(self,kwargs): #record,table_name,description
        self.request = kwargs.get('request')
        self.record = kwargs.get('record')
        print("Record ", self.record)
        self.audit = {"table_name":kwargs.get('table_name'),
                    "record_id":self.record.id,
                    "created_date":self.record.created_date,
                    "created_by":self.request.user.email,
                    "updated_date":self.record.edited_date,
                    "updated_by":self.request.user.email,
                    "description":kwargs.get("description")}
    
    def create_user_audit(self,store_state=True):
        pass
        print("Audit ====> ", self.audit)
        try:
            with transaction.atomic():
                created = Audits.objects.create(**self.audit)
                created.save()
                created_id = created.id
                return created_id
        
        except Exception as e:
            response = {"status":False,"message":f"Could not create audit... {str(e)}"} 
            return response