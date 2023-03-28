import json, uuid
from .models import CaadHeader, CaadLineItems, CaadApprovalHistory
from audit.audithelper import AuditLogView
# from .mailservice import check_recipient_send_mail
from django.db import transaction
# from ..settings import REFUND_THRESHOLDS
from rest_framework.response import Response
from django.utils import timezone
from .tests import *
from django.shortcuts import get_object_or_404

from helper import generate_slug, get_field_name, get_permission_hierarchy,get_user_position_code
from caad.approvals.bha_approval import handle_bha_approval
from caad.approvals.first_approval import handle_first_approval
from caad.approvals.second_approval import handle_second_approval
from caad.approvals.third_approval import handle_third_approval
from caad.approvals.fourth_approval import handle_fourth_approval
from caad.approvals.fifth_approval import handle_fifth_approval
from caad.approvals.sixth_approval import handle_sixth_approval
from tasks.models import UserTasksInbox
from tasks.__task__email import send_outward_mail


class CaadHelper(object):
    """
    Helper class for creating CAAD (Centralized Accounts and Approvals Dashboard) records.
    """
    
    def __init__(self,request):
        self.request = request
    
    def create_refund_view(self,**kw):
        """
        Create a new refund item and associated CAAD records.

        Args:
            data (dict): The data to create the refund item.

        Returns:
            A Response object with a status and message indicating whether the operation was successful.
        """
        try:
            with transaction.atomic():
                data = self.request.data
                print(data)
                headers = data['header']
                headers['status'] = True
                headers['created_by'] = self.request.user.email
                headers['created_date'] = timezone.now()
                line_items = data['line_items']
                header = CaadHeader.objects.create(**headers)

                AuditLogView({
                    "request":self.request,
                    "table_name": "caad_header",
                    "record": header,
                    "description": f"A new refund item was created by {self.request.user.email}"
                }).create_user_audit(store_state=True)
                
                line_items = [
                    CaadLineItems(header_id=header.pk, **line_item)
                    for line_item in line_items
                ]

                CaadLineItems.objects.bulk_create(line_items)
                approval_history = CaadApprovalHistory.objects.create(
                    header_id=header.pk,
                    creator= self.request.user.email,
                    creator_role=get_user_position_code(self.request.user.position)
                )

                bhas_list = User.objects.filter(business_unit__icontains=self.request.user.business_unit).filter(position__icontains='BHA').values('email')
                bhas = []
                for bha in bhas_list:
                    bhas.append(bha.get('email'))
                mail_parameters = {"ir_template":"caad_validate",
                    "url":"",
                    "subject":"Customer Account Adjustment Document Validation",
                    "sender":self.request.user.email, 
                    "body":data,
                    "recipients":bhas}
                print("Mail parameter ====> ", mail_parameters)
                task = {"user":get_object_or_404(User,email=bhas[0]),"taskid":uuid.uuid4(),
                "task_description":f"CAAD validation for {data['header'].get('customer_name')}",
                "task_sentby":self.request.user.email,"created_by":self.request.user.email,"associated_customer":data['header'].get('accountno')}
                UserTasksInbox.objects.create(**task)
                send_outward_mail.delay(mail_parameters)
                response = {"status": True, "message": "New caad request was created..."}
                return Response(response) 
        
        except Exception as e:
            print(str(e))
            response = {"status":False,"message":f"Could not create caad record"} 
            return Response(response) 
    
    def caad_approval(self):
        # try:
            self.all_items = []
            self.url = ''
            data = self.request.data
            print(data, self.request.GET.get('action'))

            if int(self.request.GET.get('action')) == 0:
                copied_data = data.copy()
                header_obj = CaadHeader.objects.filter(id = int(copied_data['header']))
                header = header_obj.values()
                copied_data.pop('action')
                copied_data.pop('header')
                # copied_data.pop('error_lineitems')
                copied_data['revert_status'] = True
                copied_data['percentage_approval'] = 0.00
                header = header_obj.update(**copied_data)
                approval_history = CaadApprovalHistory.objects.filter(header_id = data['header'])
                print("----->",approval_history)
                position_code = get_user_position_code(self.request.user.position),
                approval_history.update(**{"user_action":f"{position_code} Approval","action_status":f"{position_code} APPROVED","rejected_reason":data.get('revert_comments')})
                print(type(header))
                if header:
                    self.audit_log = AuditLogView({"table_name":"caad_header",
                                                "record":get_object_or_404(CaadHeader,id=data['header']),
                                                "request":self.request,
                                                "description":f"Caad record was reverted by {self.request.user.email}"
                                            })
                    self.audit_log.create_user_audit(store_state=True)
                
                # line_item_db_all = CaadLineItems.objects.filter(header_id = int(copied_data['header'])).values()
                # if len(line_item_db_all > 0):
                #     for item in line_item_db_all:
                #         self.all_items.append(item.get('id'))
                #     # Update records with the same value
                #     CaadLineItems.objects.filter(id__in=data['error_lineitems']).update(error_flag=True)
                    
                #     update_ids = [x for x in self.all_items if x not in data['error_lineitems']]
                #     CaadLineItems.objects.exclude(id__in=update_ids).update(error_flag=False)
                    
                response = {"status":True,"message":"Caad record was reverted..."} 
                return Response(response)
            
            if int(self.request.GET.get('action')) == 1:
                header = data.get('header')
                print(header,header)
                request_user_position_code = get_user_position_code(self.request.user.position)
                caad_header = CaadHeader.objects.get(id = header)
                print(caad_header)
                refund_amount = caad_header.refund_amount
                percent_base = get_percentage_base(refund_amount)

                approvals = {
                    'BHA':handle_bha_approval,
                    'BHM': handle_first_approval,
                    'OC': handle_second_approval,
                    'RH': handle_third_approval,
                    'HCS': handle_fourth_approval,
                    'CCO': handle_fifth_approval,
                    'MD': handle_sixth_approval,
                }
                
                handle_approval = approvals.get(request_user_position_code)
                print(caad_header,request_user_position_code,request_user_position_code != 'BHA',percent_base)
                # self.request.data['header_id'] = header
                if handle_approval and request_user_position_code != 'BHA':
                    response_data = handle_approval(self.request,header,percent_base,refund_amount)
                else:
                    print(000000000)
                    response_data = handle_approval(self.request,header,0,0.00)
                if not response_data:
                    response_data['percent_base'] = percent_base
                    response_data['success'] = True
                    response_data['status'] = True                    

                return Response(response_data)
      
        # except Exception as e:
        #     print(str(e))
        #     response = {"status":False,"message":f"Could not perform this operation... {str(e)}"} 
        #     return json.dumps(response) 
    
        
    # @http.route('/cms/caad/update_refund/',website=True,auth='user')
    # def update_refund_view(self,id,data,**kw):
    #     try:
    #         id = int(id)
    #         data = json.loads(data)
    #         if data['headers']['is_metered'] != True and data['headers']['is_metered'] != str(1):
    #             data['headers']['is_metered'] = False
    #         header = request.env['caad.header'].sudo().search([('id','=',id)])
    #         data['headers']['status'] = True
    #         header[0].sudo().write(data['headers'])
    #         if header:
    #             self.audit_log = AuditLogView({"table_name":"caad_header",
    #                                         "record":header,
    #                                         "description":f"A caad record was updated by {request.env.user.login}"
    #                                     })
    #             self.audit_log.create_user_audit(store_state=True)
    #         if (isinstance(header[0].id, int)):
    #             for line_item in data['line_items']:
    #                 line_item['header_id'] = int(header[0].id)
    #                 if line_item['id'] is not None:
    #                     line_item_db = request.env['caad.line_items'].sudo().search([('id','=',int(line_item['id']))])
    #                     line_item_db.sudo().write(line_item)
    #                     # if len(line_item) > 0:
    #                     #     self.line_item = AuditLogView({"table_name":"caad_line_item",
    #                     #                                 "record":line_item,
    #                     #                                 "description":f"A caad record line item was updated by {request.env.user.login}"
    #                     #                             })
    #                     #     self.audit_log.create_user_audit(store_state=True)
    #                 else:
    #                     line_item.pop('id')
    #                     line_item['header_id'] = int(header[0].id)
    #                     request.env['caad.line_items'].sudo().create(line_item)
    #                     # if len(line_item) > 0:
    #                     #     self.audit_log = AuditLogView({"table_name":"caad_line_item",
    #                     #                                 "record":line_item,
    #                     #                                 "description":f"A caad record line item was created while updating, action by {request.env.user.login}"
    #                     #                             })
    #                     #     self.audit_log.create_user_audit(store_state=True)
            
    #         response = {"status":True,"message":"Caad request was updated..."} 
    #         return json.dumps(response, default=Serializables.jsonSerializer) 
        
    #     except Exception as e:
    #         response = {"status":False,"message":f"Could not create options... {str(e)}"} 
    #         return json.dumps(response, default=Serializables.jsonSerializer) 
        
    # @http.route('/cms/caad/pending_queue/',website=True,auth='user')
    # def caad_pending_queue(self,**kw):
    #     self.set_and_get_permissions()
    #     dev_perm = Permissions.checkDeveloperPermissions(http.request.env.user)
    #     create_perm = Permissions.checkPermissions(http.request.env.user)
    #     caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
    #     try:
    #         locale_positions = ['BHM','OC','RH']
    #         last_approvals = {"BHM":"","OC":"BHM APPROVED","RH":"OC APPROVED","HCS":"RH APPROVED","CCO":"HCS APPROVED","MD":"CCO APPROVED"}
    #         buid = http.request.env.user.business_unit
    #         user_position = http.request.env.user.position
    #         if user_position in locale_positions:
    #             pending_queue = request.env['caad.header'].sudo().search([(self.key, '=', self.permissions_dict[self.key]),('last_approval', '=', last_approvals[user_position])], order="write_date desc") if self.key != 'hq' else request.env['caad.header'].sudo().search([], order="write_date desc")
    #         else:
    #             pending_queue = request.env['caad.header'].sudo().search([('last_approval', '=', last_approvals[user_position])], order="write_date desc") if self.key != 'hq' else request.env['caad.header'].sudo().search([], order="write_date desc")
    #         return request.render("cms_ibedc.caad_approval",{'user_position':http.request.env.user.position,'rendered':True,
    #                                                          "can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
    #                                                          'pending_queue':pending_queue,'dev_perm':dev_perm,
    #                                                          'create_perm':create_perm,'caad_perm':caad_perm,
    #                                                          'key':self.key,'permissions_dict':self.permissions_dict,"this":self,
    #                                                          'position':http.request.env.user.position,
    #                                                          })
            
    #     except Exception as e:
    #         response = {"status":False,"message":f"Your role does not have permission to view this page"} 
    #         return json.dumps(response, default=Serializables.jsonSerializer) 
        
    # @http.route('/cms/caad/filter_pending_queue/',website=True,auth='user')
    # def caad_filter_pending_queue(self,**kw):
    #     dev_perm = Permissions.checkDeveloperPermissions(http.request.env.user)
    #     create_perm = Permissions.checkPermissions(http.request.env.user)
    #     caad_perm = Permissions.checkCaadApprovalPermissions(http.request.env.user)
    #     try:
    #         buid = http.request.env.user.business_unit
    #         if self.hq_user:
    #             pending_queue = request.env['caad.header'].sudo().search([('is_reverted', '=', True)])
    #         else:
    #             pending_queue = request.env['caad.header'].sudo().search([('business_hub', '=', buid),('is_reverted', '=', True)])
    #         return request.render("cms_ibedc.caad_approval",{'user_position':http.request.env.user.position,'rendered':True,"can_approve":Permissions.checkCustomerApprovalPermissions(http.request.env.user),
    #                                                        'pending_queue':pending_queue,'dev_perm':dev_perm,'create_perm':create_perm,"position":self.http_request.env.user.position,
    #                                                        'caad_perm':caad_perm,})
            
    #     except Exception as e:
    #         response = {"status":False,"message":f"Could not create options... {str(e)}"} #['BHM', 'MD', 'RH', 'HCS', 'CCO', 'OC']
    #         return json.dumps(response, default=Serializables.jsonSerializer) 
        
    # @http.route('/cms/caad/get_caad_lineitems/',website=True,auth='user')
    # def get_line_items(self,data,**kw):
    #     try:
    #         data = json.loads(data)
    #         header = request.env['caad.header'].sudo().search([('id', '=', int(data['header']))])
    #         header = self.convert_record_to_dict(header)
    #         line_items = request.env['caad.line_items'].sudo().search([('header_id', '=', int(data['header']))], order="write_date desc")
    #         line_items = self.convert_record_to_dict(line_items)
    #         approval_history = request.env['caad.approval_history'].sudo().search([('header_id', '=', int(data['header']))], order="write_date desc")
    #         approval_history = self.convert_record_to_dict(approval_history)
    #         self.position = http.request.env.user.position
    #         return json.dumps({"status":True,"message":f"Retrieved line items and headers",'header':header,'line_items':line_items,'approval_history':approval_history,'user_position':self.position},default=Serializables.jsonSerializer)
            
    #     except Exception as e:
    #         response = {"status":False,"message":f"Could not create options... {str(e)}"} 
    #         return json.dumps(response, default=Serializables.jsonSerializer) 
    
    # def request_approval_mail(self,position,data,url,action='accept'):
    #     self.set_and_get_permissions()
    #     locale_positions = ['BHM','OC','RH']
    #     url = url.replace("/cms/caad/approval/","")
    #     data['account_no_url'] = f"{url}/cms/customer_details/?component=caad&queryParam={data['account_no']}&action=update&header={data['header']}#new-caad-request"

    #     if position != '':
    #         mail_template = 'caad_approval_mail' if action == 'accept' else 'declined_approval_mail'
    #         if position in locale_positions:
    #             key = 'region' if self.key == 'state' else None
    #             mail_users = request.env['res.users'].sudo().search([('position', '=', position),(f'{key}', '=', f'{self.permissions_dict[self.key]}')], order="write_date desc")
    #         else:
    #             mail_users = request.env['res.users'].sudo().search([('position', '=', position)], order="write_date desc")
            
    #     for mail_user in mail_users:
    #         data['refund_amount'] = '₦' + '{:,}'.format(data['refund_amount'])
    #         check_recipient_send_mail(self,{'login':mail_user.login,'template':mail_template},data)
    
   
    # def convert_record_to_dict(self,records):
    #     options_object_list = []
    #     models_ids = records
    #     for model in models_ids:
    #         new_dict = model.read()[0]
    #         options_object_list.append(new_dict)
    #     return options_object_list

    # def set_and_get_permissions(self):
    #     self.http_request = http.request
    #     self.service_center_user = self.http_request.env.user.is_servicecenter_user()
    #     self.business_unit_user = self.http_request.env.user.is_businesshub_level_user()
    #     self.regional_user = self.http_request.env.user.is_regional_level_user()
    #     self.hq_user = self.http_request.env.user.is_headquarters_level_user()
    #     self.permissions_dict = {'state':self.http_request.env.user.region,'buid':self.http_request.env.user.business_unit,'servicecenter':self.http_request.env.user.service_center,'bucode':self.http_request.env.user.bucode,'hq':'GRANTED'}
        
    #     if self.hq_user :
    #         self.key = 'hq'            
    #     elif self.regional_user :
    #         self.key = 'state'
    #         self.PERMISSION = f"""{self.key} ilike '{self.permissions_dict[self.key]}'"""
    #     elif self.business_unit_user:
    #         self.key = 'buid' 
    #         self.PERMISSION = f"""{self.key} ilike ('{self.permissions_dict[self.key]}','{self.permissions_dict["bucode"]}')"""
    #     elif self.service_center_user:
    #         self.key = 'servicecenter'
    #         self.PERMISSION = f"""{self.key} ilike '{self.permissions_dict[self.key]}'"""

  