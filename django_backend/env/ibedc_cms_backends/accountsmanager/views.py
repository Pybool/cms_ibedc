from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomerDrafts, CustomerEditQueue
import datetime
from authentication.models import User
from audit.audithelper import *
from django.utils import timezone
from .account_generator import generate_account_no
from rest_framework.views import APIView
from helper import DotAccessibleDict
from rest_framework.response import Response
from authentication.cms_authenticate import JWTAuthenticationMiddleWare
from customer.models import EcmiCustomersNew, EmsCustomersNew
from tasks.__task__email import send_outward_mail


class CustomerEditQueueView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def post(self,request):
        try:
            data = request.data
            # if not EcmiCustomersNew.objects.filter(accountno=data['accountno']).exists() and not EmsCustomersNew.objects.filter(accountno=data['accountno']).exists():
            email_exists = CustomerEditQueue.objects.filter(email=data['email']).values()
            mobile_exists = CustomerEditQueue.objects.filter(mobile=data['mobile']).values()
            accountno_exists = CustomerEditQueue.objects.filter(customer_id=data['accountno']).values()
            queues = {'email_exists': email_exists, 'mobile_exists': mobile_exists, 'accountno_exists': accountno_exists}
            
            for queue_type, queue in queues.items():
                queue_list = []
                for item in queue:
                    item = DotAccessibleDict(item)
                    queue_list.append({'id': item.id, 'firstname': item.firstname, 'surname': item.surname, 'othernames': item.othernames, 'email': item.email, 'mobile': item.mobile, 'region': item.region, 'buid': item.buid, 'servicecenter': item.servicecenter, 'created_date': item.created_date, 'edited_date': item.edited_date})
                queues[queue_type] = queue_list
            if email_exists or mobile_exists or accountno_exists:
                response = {'status': True, 'message': 'There are very similar record(s) with either the same Email, Phone number or Account no as this draft being submitted', 'exists': True, 'data': queues}
            else:
                awaiting_customer = data
                awaiting_customer.pop('customer')   
                awaiting_customer['name'] = awaiting_customer.get('firstname') + ' ' +  awaiting_customer.get('surname')
                awaiting_customer['accountno'] = generate_account_no()
                awaiting_customer['othernames'] = awaiting_customer.pop('othernames')
                awaiting_customer['edited_by'] = request.user.email
                awaiting_customer['customer_created_by'] = request.user.email
                awaiting_customer['created_by'] = request.user.email
                awaiting_customer['edited_date'] = timezone.now()
                awaiting_customer['approved'] = False
                awaiting_customer['approved_by'] = ''
                awaiting_customer['status'] = 'Pending'
                awaiting_customer['is_fresh'] = True
                awaiting_customer['is_draft'] = False
                awaiting_customer['address1'] =awaiting_customer.pop('address')
                awaiting_customer['meter_oem'] = awaiting_customer.pop('meteroem')
                
                customer = CustomerEditQueue.objects.create(**awaiting_customer)
                if customer.id:
                    self.audit_log = AuditLogView({"table_name":"customer_drafts",
                                                    "record":customer,"request":request,
                                                    "description":f"Awaiting customer {customer.name} was created in approval queue by modal action by {request.user.email}"
                                                 })
                    self.audit_log.create_user_audit()
                    """Audit ths action at this point"""
                    users = User.objects.filter(region=awaiting_customer['state'],business_unit=awaiting_customer['buid'],position__icontains='BHM').values('email')
                    print("++++++ ",users)
                    emails = []
                    for user in users:
                        emails.append(user.get('email'))
                    print(emails)
                    mail = {"ir_template":"crmd_creation",
                            "url":"",
                            "subject":"Customer Record Modification Document Creation",
                            "sender":'noreply@ibedc.com', 
                            "recipients":emails}
                    
                    send_outward_mail.delay(mail)
                response = {'status': True, 'message': 'This new record is now awaiting approval', 'data':str(customer.__dict__), 'exists': False}

            return Response(response)
        except Exception as e:
            print(str(e))
            return Response({"status":False,"message":'Something went wrong while creating this Awaiting Customer'})

    def put(self,request):
        try:
            base_data = request.data
            
            data = base_data.get('data')
            data.pop('customer')
            force = data.get('force')
            print("Force ===> ", force)
            if force == False:
                awaiting_customer = CustomerEditQueue.objects.filter(id=base_data.get('rowid')).exists()
                print(awaiting_customer)
                if awaiting_customer:
                    
                    data['cms_created'] =  True
                    data['edited_by'] = request.user.email
                    data['edited_date'] = timezone.now()
                    data['approved'] = False
                    data['approved_by'] = ''
                    data['status'] = 'Pending'
                    data['is_fresh'] = False
                    data['is_draft'] = False
                    data['address1'] = data.pop('address')
                    try:
                        data['meter_oem'] = data.pop('meteroem')
                    except:
                        pass
                    data.pop('force')
                    draft_cursor = CustomerEditQueue.objects.filter(id=base_data.get('rowid'))
                    if draft_cursor:
                        print(draft_cursor)
                        draft_cursor.update(**data)
                        response = {
                            "status": True,
                            "message": f"Draft customer was updated and pending with account no {draft_cursor.values('accountno').first().get('accountno')}",
                            "exists": True,
                        }
                    else:
                        response = {"status": False, "message": "Draft customer was not found", "exists": False}
                   
            elif force == True:
                
                data['accountno'] =  generate_account_no()
                data['cms_created'] =  True
                data['edited_by'] = request.user.email
                data['created_by'] = request.user.email
                data['customer_created_by'] = request.user.email
                data['edited_date'] = timezone.now()
                data['approved'] = False
                data['approved_by'] = ''
                data['status'] = 'Pending'
                data['is_fresh'] = True
                data['is_draft'] = False
                data['address1'] = data.pop('address')
                data['meter_oem'] = data.pop('meteroem')
                data.pop('force')
               
                CustomerEditQueue.objects.create(**data)
                response = {"status": True, "message": "This new record is now awaiting approval", "exists": False}
            else:
                response = {"status": False, "message": "Invalid force parameter", "exists": False}

            return JsonResponse(response)

        except Exception as err:
            response = {"error": str(err)}
            return JsonResponse(response)
