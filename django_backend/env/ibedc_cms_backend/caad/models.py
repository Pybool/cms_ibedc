from django.db import models

USER_ACTION_CHOICES = [
('BHM Approval','BHM Approval'),
('OC Approval', 'OC Approval'),
('RH Approval', 'RH Approval'),
('HCS Approval', 'HCS Approval'),
('CCO Approval', 'CCO Approval'),
('MD Approval', 'MD Approval')
]

ACTION_STATUS_CHOICES = [
('RH APPROVED', 'RH APPROVED'),
('OC APPROVED', 'OC APPROVED'),
('HCS APPROVED', 'HCS APPROVED'),
('CCO APPROVED', 'CCO APPROVED'),
('BHM APPROVED', 'BHM APPROVED'),
('MD APPROVED', 'MD APPROVED')
]

class CaadHeader(models.Model):
    account_no = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    buid = models.CharField(max_length=255)
    bucode = models.CharField(max_length=255)
    total_accrued = models.FloatField()
    vat = models.FloatField()
    current_outstanding_bal = models.FloatField()
    refund_amount = models.FloatField()
    is_metered = models.BooleanField()
    total_estimate = models.FloatField()
    status = models.BooleanField(default=False)
    revert_comments = models.TextField(default='')
    state = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    servicecenter = models.CharField(max_length=255)
    percentage_approval = models.FloatField(default=0.00)
    last_approval = models.CharField(max_length=255, default='')
    created_date = models.DateTimeField(verbose_name='Created Date', null=True, blank=True)
    created_by = models.CharField(max_length=255, verbose_name='Created By', null=True, blank=True)
    edited_date = models.DateTimeField(verbose_name='Edited Date', null=True, blank=True)

class CaadLineItems(models.Model):
    header = models.ForeignKey(CaadHeader, related_name='lineitems', on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    months = models.IntegerField()
    tarrif = models.FloatField()
    recom_unit = models.FloatField()
    mab = models.FloatField()
    ebm = models.FloatField()
    error_flag = models.BooleanField(default=False)
    index = models.CharField(max_length=255, default='')
    uuid = models.CharField(max_length=255, default='')
    
    #ONLY FOR METERED CUSTOMERS
    present_reading = models.FloatField(default=0.00)
    last_actual_reading = models.FloatField(default=0.00)
    consumed = models.FloatField(default=0.00)
    edited_date = models.DateTimeField(verbose_name='Edited Date', null=True, blank=True)

class CaadApprovalHistory(models.Model):
    header = models.ForeignKey(CaadHeader, on_delete=models.CASCADE)
    creator = models.CharField(max_length=255)
    creator_role = models.CharField(max_length=255)
    bhm_compliance = models.BooleanField(default=False)
    operation_compliance = models.BooleanField(default=False)
    completed_approval_sequence = models.BooleanField(default=False)
    user_action = models.CharField(choices=USER_ACTION_CHOICES, null=True, max_length=255)
    action_status = models.CharField(choices=ACTION_STATUS_CHOICES, max_length=255)
    rejected_reason = models.CharField(max_length=255, default='')
    percentage_approval = models.FloatField(default=0.00)
    created_date = models.DateTimeField(verbose_name='Created Date', null=True, blank=True)
    created_by = models.CharField(max_length=255, verbose_name='Created By', null=True, blank=True)
    edited_date = models.DateTimeField(verbose_name='Edited Date', null=True, blank=True)
    
class CaadApprovalUsers(models.Model):
    caad = models.ForeignKey(CaadHeader, on_delete=models.CASCADE)
    approver_name = models.CharField(max_length=255)
    approver_position = models.CharField(max_length=255)
    approver_email = models.CharField(max_length=255)
    date_approved = models.DateTimeField(auto_now_add=True)
    comments = models.CharField(max_length=255)