from django.db import models

class CustomerEditQueue(models.Model):
    name = models.CharField(max_length=255, default='')
    customer_id = models.CharField(max_length=255,default='0')
    accountno = models.CharField(max_length=255, default='')
    firstname = models.CharField(max_length=255, default='')
    surname = models.CharField(max_length=255, default='')
    othernames = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=255, default='')
    mobile = models.CharField(max_length=255, default='')
    address1 = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    statuscode = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    building_description = models.CharField(max_length=255, default='')
    lga = models.CharField(max_length=255, default='')
    premise_type = models.CharField(max_length=255, default='')
    region = models.CharField(max_length=255, default='')
    buid = models.CharField(max_length=255, default='')
    servicecenter = models.CharField(max_length=255, default='')
    customer_type = models.CharField(max_length=255, default='')
    accounttype = models.CharField(max_length=255, default='')
    business_type = models.CharField(max_length=255, default='')
    landlord_name = models.CharField(max_length=255, default='')
    landlord_phone = models.CharField(max_length=255, default='')
    injection_sub_station = models.CharField(max_length=255, default='')
    meter_oem = models.CharField(max_length=255, default='')
    cin = models.CharField(max_length=255, default='')
    feeder_name = models.CharField(max_length=255, default='')
    feeder_type = models.CharField(max_length=255, default='')
    service_band = models.CharField(max_length=255, default='')
    upriser_id = models.CharField(max_length=255, default='')
    dss_id = models.CharField(max_length=255, default='')
    dss_name = models.CharField(max_length=255, default='')
    dss_owner = models.CharField(max_length=255, default='')
    feeder_type = models.CharField(max_length=255, default='')
    feeder_name = models.CharField(max_length=255, default='')
    feederid = models.CharField(max_length=255, default='')
    ltpoleid = models.CharField(max_length=255, default='')
    
    created_by = models.CharField(max_length=255, default='')
    created_date = models.DateField(auto_now_add=True,blank=True,null=True)
    edited_by = models.CharField(max_length=255, default='')
    edited_date = models.DateField(auto_now=True,blank=True,null=True)
    
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=255, default='')
    approved_date = models.DateField(auto_now_add=True,blank=True,null=True)
    
    status = models.CharField(max_length=255, default='')
    comments = models.TextField(default='')
    cms_created = models.BooleanField(default=False)
    is_fresh = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    customer_created_by = models.CharField(max_length=255, default='')
    #Approval Fields
    bhm_aproved = models.BooleanField(default=False)
    auditor_approved = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'customer_editqueue'
    

class CustomerDrafts(models.Model):
    draft_tag = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    customer_id = models.IntegerField(default=0)
    accountno = models.CharField(max_length=255, default='')
    firstname = models.CharField(max_length=255, default='')
    surname = models.CharField(max_length=255, default='')
    othernames = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=255, default='')
    mobile = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    address1 = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    statuscode = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=255, default='')
    building_description = models.CharField(max_length=255, default='')
    lga = models.CharField(max_length=255, default='')
    premise_type = models.CharField(max_length=255, default='')
    region = models.CharField(max_length=255, default='')
    buid = models.CharField(max_length=255, default='')
    servicecenter = models.CharField(max_length=255, default='')
    customer_type = models.CharField(max_length=255, default='')
    accounttype = models.CharField(max_length=255, default='')
    business_type = models.CharField(max_length=255, default='')
    landlord_name = models.CharField(max_length=255, default='')
    landlord_phone = models.CharField(max_length=255, default='')
    injection_sub_station = models.CharField(max_length=255, default='')
    meter_oem = models.CharField(max_length=255, default='')
    cin = models.CharField(max_length=255, default='')
    feeder_name = models.CharField(max_length=255, default='')
    feeder_type = models.CharField(max_length=255, default='')
    service_band = models.CharField(max_length=255, default='')
    upriser_id = models.CharField(max_length=255, default='')
    dss_id = models.CharField(max_length=255, default='')
    dss_name = models.CharField(max_length=255, default='')
    dss_owner = models.CharField(max_length=255, default='')
    feeder_type = models.CharField(max_length=255, default='')
    feeder_name = models.CharField(max_length=255, default='')
    feederid = models.CharField(max_length=255, default='')
    ltpoleid = models.CharField(max_length=255, default='')
    
    created_by = models.CharField(max_length=255, default='')
    created_date = models.DateField(auto_now_add=True,blank=True,null=True)
    edited_by = models.CharField(max_length=255, default='')
    edited_date = models.DateField(auto_now=True,blank=True,null=True)
    
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=255, default='')
    approved_date = models.DateField(auto_now_add=True,blank=True,null=True)
    
    status = models.CharField(max_length=255, default='')
    comments = models.TextField(default='')
    cms_created = models.BooleanField(default=False)
    is_fresh = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    customer_created_by = models.CharField(max_length=255, default='')
    #Approval Fields
    bhm_aproved = models.BooleanField(default=False)
    auditor_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'customer_drafts'
