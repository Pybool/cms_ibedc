from helper import DotAccessibleDict
from rest_framework.response import Response
from accountsmanager.models import CustomerEditQueue
from customer.models import EcmiCustomersNew, EmsCustomersNew
from authentication.models import User
from tasks.__task__email import *
from django.db.models import Q
url = ''
values = ['bhm_aproved','auditor_approved','name', 'accountno', 'firstname', 'surname', 'othernames', 'email', 'mobile', 'region', 'buid', 'city', 'state', 'dss_id', 'dss_name', 'dss_owner', 'statuscode', 'title', 'gender', 'building_description', 'lga', 'premise_type', 'region', 'customer_type', 'accounttype', 'business_type', 'landlord_name', 'landlord_phone', 'injection_sub_station', 'meter_oem', 'cin', 'feeder_name', 'service_band', 'upriser_id', 'feederid', 'feeder_type', 'ltpoleid', 'servicecenter', 'cms_created', 'customer_created_by']

class Approvals(object):
    
    def __init__(self,args) -> None:
        args = DotAccessibleDict(args)
        print("args", args)
        self.field_name = args.field_name
        self.location = args.location
        self.user_position_code = args.position_code
        
    def remove_non_field_data(self,data):
        clone = data.copy()
        data.pop('id')
        data.pop('action')
        return clone, data
    
    def clean_fields(self,vals):
        vals.pop('name')
        vals.pop('bhm_aproved')
        vals.pop('auditor_approved')
        return vals
    
    def sanitize_fields(self,awaiting_customer,values,accountno):
        if awaiting_customer.values('accounttype').first().get('accounttype') == 'Postpaid':
            values.append('address1') 
            vals = CustomerEditQueue.objects.filter(accountno=accountno).values(*values).first()# awaiting_customer.values().first()
        else:
            values.append('address1')
            vals = CustomerEditQueue.objects.filter(accountno=accountno).values(*values).first()# awaiting_customer.values().first()
            vals['address'] = vals.pop('address1')
        vals['meteroem'] = vals.pop('meter_oem')
        vals['upriserid'] = vals.pop('upriser_id')
        
        return vals
    
    def treat_as_fresh(self,data):
        accountno = data.get('accountno')
        awaiting_customer = CustomerEditQueue.objects.filter(accountno=accountno).filter(**{f"{self.field_name}__icontains": self.location})
        o_awaiting_customer = awaiting_customer
        data, clone = self.remove_non_field_data(data)
        if data['action'] == 'approve':
            
            if self.user_position_code== 'BHM':
                clone['bhm_aproved'] = True 
                # clone['bhm_approver'] 
                awaiting_customer.update(**clone)
                 
                """Audit ths action at this point"""
                users = User.objects.filter(Q(region=o_awaiting_customer.values().first().get('region')) | Q(business_unit=o_awaiting_customer.values().first().get('buid')),position__icontains='ADT').values('email')

                emails = []
                for user in users:
                    emails.append(user.get('email'))
                print(emails)
                mail = {"ir_template":"crmd_approval",
                        "url":"",
                        "subject":"Customer Record Modification Document Approval",
                        "sender":'noreply@ibedc.com', 
                        "recipients":emails}
                
                send_outward_mail.delay(mail)
                response = {"status":True,"message":"Action completed succesfully"}  
            
            elif self.user_position_code== 'ADT':
                print("########################")
                with transaction.atomic():
                    clone['auditor_approved'] = True
                    clone['cms_created'] = True
                    clone['approved'] = True if data['action'] == 'approve' else False
                    awaiting_customer.update(**clone)
                    """Audit ths action at this point"""
                    user = o_awaiting_customer.values().first().get('approved_by')
                    emails = []
                    emails.append(user)
                    emails.append(awaiting_customer.values().first().get('created_by'))
                    print(emails)
                    # return 
                    mail = {"ir_template":"crmd_approval",
                            "url":"",
                            "subject":"Customer Record Modification Document Approvals Completed",
                            "sender":'noreply@ibedc.com', 
                            "recipients":emails}
                    
                    send_outward_mail.delay(mail)
                    response = {"status":True,"message":"Action completed succesfully"}  
            
                    vals = self.sanitize_fields(awaiting_customer,values,accountno)
                    print("checks--> ",data['action'] == 'approve' , vals.get('bhm_aproved')==True , vals.get('auditor_approved')==True)
                    if data['action'] == 'approve' and vals.get('bhm_aproved') and vals.get('auditor_approved'):
                        vals = self.clean_fields(vals)
                        awaiting_customer_data = vals                
                        # vals['accountno'] = '2039000000001'
                        if awaiting_customer_data.get('accounttype') not in ['Prepaid', 'Postpaid']:
                            return Response({'status':False, 'message':'Invalid account type in parameters'})
                        
                        """Ensure customer with given account no does not exist in either Ems or Ecmi customer tables"""
                        print(vals['accountno'])
                        if not EcmiCustomersNew.objects.filter(accountno=vals['accountno']).exists() and not EmsCustomersNew.objects.filter(accountno=vals['accountno']).exists():
                            EcmiCustomersNew.objects.create(**awaiting_customer_data) if awaiting_customer_data.get('accounttype') == 'Prepaid' else EmsCustomersNew.objects.create(**awaiting_customer_data)
                            created_customer = EcmiCustomersNew.objects.filter(accountno=vals['accountno']).values('accountno')
                            clone['customer_id'] = created_customer[0].get('accountno','0')
                            clone['accountno'] = created_customer[0].get('accountno','0')
                            clone['is_fresh'] = False                
                            awaiting_customer.update(**clone) #Update customer awaiting queue
                            """Audit ths action at this point"""
                            response = {"status":True,"message":"Action completed successfully, new customer has been created"}  
                        else:
                            return Response({'status':False, 'message':'this customer already exists, could not create new customer with this account number'})
                
            return Response(response)
            
        
        elif data['action'] == 'decline':
            if self.user_position_code== 'BHM':
                clone['bhm_aproved'] = False 
            elif self.user_position_code== 'ADT':
                clone['auditor_approved'] = False
            clone['status'] = 'Declined'
            clone['is_draft'] = True
            declined_customer = CustomerEditQueue.objects.filter(accountno=accountno)
            declined_customer.update(**clone)
            """Audit ths action at this point"""
            response = {"status":True,"message":"This new customer has been declined"}  
            return Response(response)
        return Response(response)     
                 
    def treat_as_unfresh(self,data):
        if self.field_name != 'hq':
            """Get from awaiting customer queue already an existing customer and filter based on user hierarchy"""
            awaiting_customer = CustomerEditQueue.objects.filter(customer_id = data.get('customer_id'),accountno=data.get('accountno')).filter(**{f"{self.field_name}__icontains": self.location}) 
        else:
            """Get from awaiting customer queue already an existing customer no hierarchy implemented for HQ user"""
            awaiting_customer = CustomerEditQueue.objects.filter(customer_id = data.get('customer_id'))
            
        if awaiting_customer: 
            if data['action'] == 'approve':
                data, clone = self.remove_non_field_data(data)
                if self.user_position_code== 'BHM':
                    clone['bhm_aproved'] = True 
                    awaiting_customer.update(**clone)
                    """Audit ths action at this point"""
                                        
                elif self.user_position_code== 'ADT':
                    clone['auditor_approved'] = True 
                    awaiting_customer.update(**clone)
                    """Audit ths action at this point"""
                
                if self.field_name == 'hq':
                    clone['bhm_aproved'] = True 
                    clone['auditor_approved'] = True 
                    awaiting_customer.update(**clone)
                    """Audit ths action at this point"""
            
            
            elif data['action'] == 'decline':
                data['status'] = 'Declined'
                if self.user_position== 'BHM':
                    data['bhm_aproved'] = False
                    data['is_draft'] = True
                    awaiting_customer.update(**data)
                    """Audit ths action at this point"""
    
                elif self.user_position== 'ADT':
                    data['auditor_approved'] = False
                    awaiting_customer.update(**data)
                    """Audit ths action at this point"""
                    
                if self.field_name == 'hq':
                    clone['bhm_aproved'] = False 
                    clone['auditor_approved'] = False 
                    awaiting_customer.update(**clone)
                    """Audit ths action at this point"""
                                        
                response = {"status":True,"message":"Awaiting customer record has been declined"}  
                return Response(response)
            
            elif data['action'] == 'approve' and self.is_fresh != True and awaiting_customer.bhm_aproved and awaiting_customer.auditor_approved:
                if data.get('accounttype') != 'Prepaid' or data.get('accounttype') != 'Postpaid':
                    return Response({'status':False, 'message':'Invalid account type in parameters'})
                customer = EcmiCustomersNew.objects.filter(id=data.get('customer_id')) if data.get('accounttype') == 'Prepaid' else EmsCustomersNew.objects.filter(id=data.get('customer_id'))
                awaiting_customer_data = awaiting_customer.values()
                awaiting_customer_data.pop('feeder_name')
                awaiting_customer_data['kyc'] = 1 if self.check_kyc_compliance(awaiting_customer_data) == True else 0
                customer.update(**awaiting_customer_data)
                """Audit ths action at this point"""
                
            response = {"status":True,"message":"Action completed succesfully"}  
            return Response(response) 
            
        else:
            response = {"status":True,"message":"Customer was not found in queue"}  
            return Response(response)
    