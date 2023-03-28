from caad.models import CaadApprovalHistory, CaadHeader,CaadApprovalUsers
from helper import get_user_position_code
from caad.tests import calculate_percentage, audit_action, request_approval_mail
from django.db import transaction
from decorators import is_caad_action_exists
url = ''

@is_caad_action_exists()
def handle_bha_approval(request,header_id,percent_base=0,refund_amount=0.00):
    with transaction.atomic():
        approval_history = CaadApprovalHistory.objects.filter(header_id = header_id)
        approval_history.update(**{"user_action":"BHA Approval","action_status":"BHA APPROVED","bha_compliance":True,
                                "creator":request.user.email,"creator_role":get_user_position_code(request.user.position)
                                })
        q_header =CaadHeader.objects.filter(id = header_id)
        updated_header = q_header.update(**{"last_approval":"BHA APPROVED"})
        if updated_header:
            audit_action(request,q_header.first())
        caad_data = q_header.values('customer_name', 'account_no','state','region','servicecenter','buid','refund_amount','vat')[0]
        caad_data['header'] = header_id
        
        CaadApprovalUsers.objects.create(**{'caad_id':header_id,'approver_name':request.user.name,
                                          'approver_position':request.user.position,
                                          'approver_email':request.user.email,
                                          'comments':'Satisfactory'})
        status = request_approval_mail('BHM',caad_data,url)
        if status:
            return status
        return {"status":True,"message":"Your approval for this caad request was successful, a mail has been sent to the Business Hub Manager for further Approval"}
    