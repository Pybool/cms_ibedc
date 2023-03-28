from caad.models import CaadApprovalHistory, CaadHeader, CaadApprovalUsers
from helper import get_user_position_code
from caad.tests import calculate_percentage, audit_action, request_approval_mail
from django.db import transaction
from caad.caad_config import REFUND_THRESHOLDS
from decorators import is_caad_action_exists

url = ''
@is_caad_action_exists()
def handle_third_approval(request,header_id,percent_base,refund_amount=0.00):
    print("Slack----------")
    with transaction.atomic():
        approval_history = CaadApprovalHistory.objects.filter(header_id = header_id,operation_compliance= True)
        if refund_amount <= REFUND_THRESHOLDS['range1_upper_limit']:
            approval_history.update(**{"user_action":"RH Approval","action_status":"RH APPROVED","completed_approval_sequence":True,
                                    "creator":request.user.email,"creator_role":get_user_position_code(request.user.position),
                                    "percentage_approval":calculate_percentage(3,percent_base)
                                    })
            q_header =CaadHeader.objects.filter(id = header_id)
            q_header.update(**{"percentage_approval":calculate_percentage(3,percent_base),"last_approval":"RH APPROVED"})         
            return {"status":True,"message":"Your approval for this caad request was successful and Approval Sequence Completed"}

        approval_history.update(**{"user_action":"RH Approval","action_status":"RH APPROVED","creator":request.user.email,
                                        "creator_role":get_user_position_code(request.user.position),"percentage_approval":calculate_percentage(3,percent_base)
                                        })
        q_header =CaadHeader.objects.filter(id = header_id)
        updated_header = q_header.update(**{"percentage_approval":calculate_percentage(3,percent_base),"last_approval":"RH APPROVED"})
        if updated_header:
            audit_action(request,q_header.first()) 
        caad_data = q_header.values('customer_name', 'account_no','servicecenter','buid','refund_amount','vat')[0]
        caad_data['header'] = header_id
        CaadApprovalUsers.objects.create(**{'caad_id':header_id,'approver_name':request.user.name,
                                          'approver_position':request.user.position,
                                          'approver_email':request.user.email,
                                          'comments':'Satisfactory'})
        status = request_approval_mail('HCS',caad_data,url)
        if status:
            print("rat", status)
            return status
    return {"status":True,"message":"Your approval for this caad request was successful, a mail has been sent to the Head of Customer Support (HCS) for further Approval"}
    
