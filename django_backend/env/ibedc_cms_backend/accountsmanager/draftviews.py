import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from audit.models import *
from .models import *
from django.db import transaction
from django.shortcuts import get_object_or_404
from audit.audithelper import *
from helper import *
from authentication.cms_authenticate import JWTAuthenticationMiddleWare
# Create your views here.
class DraftsView(APIView):
# @http.route(['/cms/customer/save_draft_data/'], website=True,auth='user') cms/drafts
    authentication_classes = [JWTAuthenticationMiddleWare]
    def post(self,request):
        
        print(request.data)
        data = request.data
        id = data.get('draft_id',0)
        self.message = ''
        draft_object = data.get('draft')
        draft_object['draft_tag'] = data.get('draft_tag')
        tab = data.get('type')
        self.key, self.val = get_permission_hierarchy(request)
        draft_object[self.key] = self.val
        if self.key == 'state':
            draft_object['region'] = self.val
    
        draftcheck = CustomerDrafts.objects.filter(draft_tag=draft_object['draft_tag'])
        exists = draftcheck.exists()
                  
        with transaction.atomic():
            if not exists:
                draft_object['created_by'] = request.user.email
                draft_instance = CustomerDrafts.objects.create(**draft_object)
                draft_instance.save()
                if draft_instance:
                    self.audit_log = AuditLogView({"table_name":"customer_drafts",
                                                    "record":draft_instance,"request":request,
                                                    "description":f"New draft object was created by {request.user.email}"
                                                })
                    self.audit_log.create_user_audit()
                self.message = 'created'
                self.id = draft_instance.id

            else:
                draft_object['edited_by'] = request.user.email
                try:
                    draft_object['meter_oem'] = draft_object.pop('meteroem')
                except:
                    pass
                draftcheck.update(**draft_object)
                if draft_object:
                    self.id = draftcheck.values('id')[0]['id']
                    self.audit_log = AuditLogView({"table_name":"customer_drafts",
                                                    "record":get_object_or_404(CustomerDrafts,id=self.id),"request":request,
                                                    "description":f"Draft object was updated by {request.user.email}"
                                                })
                    self.audit_log.create_user_audit()
                    self.message = 'updated'
            
            if self.message != '':
                response = {"status":True,"message":f"{tab} draft was {self.message}","data":data,"id":self.id}  
            else:
                response = {"status":False,"message":f"{tab} draft was not saved"}  
            return Response(response)

    def get(self,request):
        key, val = get_permission_hierarchy(request)
        print("Location hierarchy ===> ",key, val)
        drafts = CustomerDrafts.objects.filter(is_draft=True,created_by=request.user.email).filter(**{f"{key}__icontains": val}).values()
        return Response({'status':True,'data':drafts})
        
        # if q=='':
        #     if self.key != 'hq':
        #         if self.key != 'buid':
        #             drafts = request.env['customer.drafts'].sudo().search([('is_draft', '=', True),(f'{self.key}', '=', f'{self.permissions_dict[self.key]}')])
        #         else:
        #             drafts = request.env['customer.drafts'].sudo().search([('is_draft', '=', True),(f'{self.key}', 'in', [f'{self.permissions_dict[self.key]}',f'{self.permissions_dict["bucode"]}'])]) 
        #     else:
        #         drafts = request.env['customer.drafts'].sudo().search([('is_draft', '=', True)])
        #     drafts = self.convert_draft_record_to_list(drafts)
        #     response = {"status":True,"data":drafts,"message":"success"}  
        #     response =  Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')
        #     response.headers['Cache-Control'] = 'no-cache'
        #     return response 
        # else:
        #     pass
        
    