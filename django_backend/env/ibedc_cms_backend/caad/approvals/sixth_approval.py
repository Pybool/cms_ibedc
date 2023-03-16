from caad.models import CaadApprovalHistory, CaadHeader, CaadApprovalUsers
from helper import get_user_position_code
from caad.tests import calculate_percentage, audit_action, request_approval_mail
from django.db import transaction
from caad.caad_config import REFUND_THRESHOLDS
url = ''

def handle_sixth_approval(request,header_id,percent_base,refund_amount=0.00):
    with transaction.atomic():
        approval_history = CaadApprovalHistory.objects.filter(header_id = header_id,action_status= 'CCO APPROVED')
        if refund_amount >= REFUND_THRESHOLDS['range4_lower_limit']:
            approval_history.update(**{"user_action":"MD Approval","action_status":"MD APPROVED","completed_approval_sequence":True,
                                    "creator":request.user.email,"creator_role":get_user_position_code(request.user.position),
                                    "percentage_approval":calculate_percentage(6,percent_base)
                                    })
            q_header =CaadHeader.objects.filter(id = header_id)
            updated_header = q_header.update(**{"percentage_approval":calculate_percentage(6,percent_base),"last_approval":"MD APPROVED"})         
            
            if updated_header:
                audit_action(request,q_header.first())
            caad_data = q_header.values('customer_name', 'account_no','servicecenter','buid','refund_amount','vat').__dict__
            caad_data['header'] = header_id
            CaadApprovalUsers.objects.create(**{'caad_id':header_id,'approver_name':request.user.name,
                                          'approver_position':request.user.position,
                                          'approver_email':request.user.email,
                                          'comments':'Satisfactory'})
            request_approval_mail('MD',caad_data,url)
            return {"status":True,"message":"Your approval for this caad request was successful and Approval Sequence Completed, a mail has been sent to all approval parties"}

        else:
            pass