from caad.models import CaadApprovalHistory, CaadHeader,CaadApprovalUsers
from helper import get_user_position_code
from caad.tests import calculate_percentage,audit_action,request_approval_mail
from django.db import transaction
url = ''

def handle_second_approval(request,header_id,percent_base,refund_amount=0.00):
    with transaction.atomic():
        
        approval_history = CaadApprovalHistory.objects.filter(header_id = header_id)
                        
        approval_history.update(**{"user_action":"OC Approval","action_status":"OC APPROVED","operation_compliance":True,
                                "creator":request.user.email,"creator_role":get_user_position_code(request.user.position),
                                "percentage_approval":calculate_percentage(2,percent_base)
                                })
        q_header =CaadHeader.objects.filter(id = header_id)
        updated_header = q_header.update(**{"percentage_approval":calculate_percentage(2,percent_base),"last_approval":"OC APPROVED"})
        if updated_header:
           audit_action(request,q_header.first())
        caad_data = q_header.values('customer_name', 'account_no','servicecenter','buid','refund_amount','vat').__dict__
        caad_data['header'] = header_id
        CaadApprovalUsers.objects.create(**{'caad_id':header_id,'approver_name':request.user.name,
                                          'approver_position':request.user.position,
                                          'approver_email':request.user.email,
                                          'comments':'Satisfactory'})
        request_approval_mail('RH',caad_data,url)
        return {"status":True,"message":"Your approval for this caad request was successful, a mail has been sent to the Regional Head (RH) for further Approval"}
    
