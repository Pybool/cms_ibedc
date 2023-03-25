from audit.audithelper import AuditLogView
from caad.caad_config import REFUND_THRESHOLDS
from tasks.__task__email import send_outward_mail
from authentication.models import User


def get_percentage_base(refund_amount):
    if refund_amount <= REFUND_THRESHOLDS['range1_upper_limit']:
        return 3
    elif refund_amount >= REFUND_THRESHOLDS['range2_lower_limit'] and refund_amount <= REFUND_THRESHOLDS['range2_upper_limit']:
        return 4
    elif refund_amount >= REFUND_THRESHOLDS['range3_lower_limit'] and refund_amount <= REFUND_THRESHOLDS['range3_upper_limit']:
        return 5
    elif refund_amount >= REFUND_THRESHOLDS['range4_lower_limit']:
        return 6

def calculate_percentage(position,percent_base):
    return round((position/percent_base) * 100)

def request_approval_mail(position,data,url):
    """The implementation below assumes the following:
    ----
    1: The positions OC, BHM and RH are service center, business hub and region bounded respectively
    2: Positions from HCS up until MD are HQ Bounded
    ----
    Code logic:
        ==> If position is OC get the OC's For the caad request servicecenter and send them mails
    
    
    
    """
    if position == 'OC':
        user = User.objects.filter(position__icontains = position).filter(servicecenter=data.get('servicecenter')).values('email').first()['email']
    print("CAAD MAIL ===> ", user)
    mail = {"ir_template":"caad_approval",
            "url":"",
            "subject":"Customer Account Adjustment Document Approval",
            "sender":'noreply@ibedc.com', 
            "recipients":[user]}
                    
    send_outward_mail.delay(mail)

def audit_action(request,updated_header):
    audit_log = AuditLogView({"table_name":"caad_header",
                                    "record":updated_header,
                                    "request":request,
                                    "description":f"This caad request has been approved by {request.user.email} as {request.user.position}"
                                    })
    audit_log.create_user_audit(store_state=False)
            