from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.models import User
from django.utils.text import slugify
import itertools, uuid
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import datetime

"""PREPAID CUSTOMERS MODEL"""

class EcmiCustomersNew(models.Model):
    accountno = models.CharField(db_column='AccountNo',primary_key=True, max_length=50)  # Field name made lowercase.
    atmaccountno = models.CharField(db_column='ATMAccountNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    meterno = models.CharField(db_column='MeterNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bookno = models.CharField(db_column='BookNo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tariffid = models.DecimalField(db_column='TariffID', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    oldaccountno = models.CharField(db_column='OldAccountNo', max_length=24, blank=True, null=True)  # Field name made lowercase.
    opendate = models.DateTimeField(db_column='OpenDate', blank=True, null=True)  # Field name made lowercase.
    surname = models.CharField(db_column='Surname', max_length=128, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=128, blank=True, null=True, default='')  # Field name made lowercase.
    othernames = models.CharField(db_column='OtherNames', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address_1', max_length=300, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=20, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMail', max_length=60, blank=True, null=True)  # Field name made lowercase.
    employer = models.CharField(db_column='Employer', max_length=50, blank=True, null=True)  # Field name made lowercase.
    officeaddr = models.CharField(db_column='OfficeAddr', max_length=255, blank=True, null=True)  # Field name made lowercase.
    officetel = models.CharField(db_column='OfficeTel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=50, blank=True, null=True)  # Field name made lowercase.
    arrearsbalance = models.DecimalField(db_column='ArrearsBalance', max_digits=13, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    buid = models.CharField(db_column='BUID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    utid = models.CharField(db_column='UTID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    transid = models.CharField(db_column='TransID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    operatorname = models.CharField(db_column='OperatorName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    picture = models.BinaryField(db_column='Picture', blank=True, null=True)  # Field name made lowercase.
    fingerprint = models.BinaryField(db_column='FingerPrint', blank=True, null=True)  # Field name made lowercase.
    fingerprintrawdata2 = models.TextField(db_column='FingerPrintRawData2', blank=True, null=True)  # Field name made lowercase.
    activated = models.BooleanField(blank=True, null=True) 
    status = models.CharField(max_length=1, blank=True, null=True)
    status1 = models.CharField(max_length=1, blank=True, null=True)
    operatormodified = models.IntegerField(db_column='OperatorModified', blank=True, null=True)  # Field name made lowercase.
    lastmodifieddate = models.DateTimeField(db_column='LastModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedcount = models.IntegerField(db_column='ModifiedCount', blank=True, null=True)  # Field name made lowercase.
    accounttype = models.CharField(db_column='AccountType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tariffcode = models.CharField(db_column='TariffCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dss_id = models.CharField(db_column='DSS_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    dss_name = models.CharField(db_column='DSS_Name', max_length=300, blank=True, null=True)  # Field name made lowercase.
    dss_owner = models.CharField(db_column='DSS_Owner', max_length=300, blank=True, null=True)  # Field name made lowercase.
    servicecenter = models.CharField(db_column='ServiceCenter', max_length=200, blank=True, null=True)  # Field name made lowercase.
    updated_at = models.DateTimeField(auto_now=True)
    kyc = models.CharField(db_column='KYC', max_length=3, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    building_description = models.CharField(db_column='Building_Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lga = models.CharField(db_column='LGA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    premise_type = models.CharField(db_column='Premise_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customer_type = models.CharField(db_column='Customer_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    statuscode = models.CharField(db_column='StatusCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    business_type = models.CharField(db_column='Business_Type', max_length=100, blank=True, null=True)  # Field name made lowercase.
    feeder_name = models.CharField(db_column='Feeder_Name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    service_band = models.CharField(db_column='Service_Band', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contactphone = models.CharField(db_column='ContactPhone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contactemail = models.CharField(db_column='ContactEmail', max_length=60, blank=True, null=True)  # Field name made lowercase.
    landlord_name = models.CharField(db_column='Landlord_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    landlord_phone = models.CharField(db_column='Landlord_Phone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tenant = models.CharField(db_column='Tenant', max_length=50, blank=True, null=True)  # Field name made lowercase.
    landlord = models.CharField(db_column='Landlord', max_length=50, blank=True, null=True)  # Field name made lowercase.
    injection_sub_station = models.CharField(db_column='Injection_Sub_Station', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cin = models.CharField(db_column='CIN', max_length=300, blank=True, null=True)  # Field name made lowercase.
    meteroem = models.CharField(db_column='MeterOEM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    upriserid = models.CharField(db_column='UpriserID', max_length=300, blank=True, null=True)  # Field name made lowercase.
    feederid = models.CharField(db_column='FeederID', max_length=300, blank=True, null=True)  # Field name made lowercase.
    feeder_type = models.CharField(db_column='FeederType', max_length=300, blank=True, null=True)  # Field name made lowercase.
    ltpoleid = models.CharField(db_column='LTPoleID', max_length=300, blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(db_column='Latitude', max_length=30, blank=True, null=True)  # Field name made lowercase.
    longitude = models.CharField(db_column='Longitude', max_length=30, blank=True, null=True)  # Field name made lowercase.
    customersk = models.IntegerField(db_column='CustomerSK', blank=True, null=True)  # Field name made lowercase.
    cms_created = models.BooleanField(db_column='CMS_Created', blank=True, null=True,default=False)  # Field name made lowercase.
    customer_created_by = models.CharField(db_column='Customer_Created_By', max_length=1000, blank=True, null=True, default='')  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'ecmi_customers_new'
    #statuscode,address1, city, dss_name, dss_owner, and the last ones in emscustomers are  added by developer
# """POSTPAID CUSTOMERS MODEL"""

class EcmiTariff(models.Model):
    tariffid = models.DecimalField(db_column='TariffID', primary_key=True, max_digits=20, decimal_places=0,default=0)  # Field name made lowercase.
    tariffcode = models.CharField(db_column='TariffCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    addeddate = models.DateTimeField(db_column='AddedDate', blank=True, null=True)  # Field name made lowercase.
    status1 = models.CharField(max_length=2, blank=True, null=True)
    oldtariffcode = models.CharField(db_column='OldTariffCode', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ecmi_tariff'
        
class EmsCustomersNew(models.Model):
    accountno = models.CharField(db_column='AccountNo', max_length=20)  # Field name made lowercase.
    booknumber = models.CharField(max_length=100, blank=True, null=True)
    oldaccountnumber = models.CharField(max_length=20, blank=True, null=True)
    meterno = models.CharField(db_column='MeterNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    surname = models.CharField(db_column='Surname', max_length=177, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=177, blank=True, null=True)  # Field name made lowercase.
    othernames = models.CharField(db_column='OtherNames', max_length=177, blank=True, null=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=50, blank=True, null=True)
    serviceaddress1 = models.CharField(db_column='ServiceAddress1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    serviceaddress2 = models.CharField(db_column='ServiceAddress2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    serviceaddresscity = models.CharField(db_column='ServiceAddressCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    serviceaddressstate = models.CharField(db_column='ServiceAddressState', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tariffid = models.IntegerField(db_column='TariffID', blank=True, null=True)  # Field name made lowercase.
    arrearsbalance = models.DecimalField(db_column='ArrearsBalance', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=20, blank=True, null=True)  # Field name made lowercase.
    methodofidentification = models.CharField(db_column='MethodOfIdentification', max_length=100, blank=True, null=True)  # Field name made lowercase.
    accttypedesc = models.CharField(db_column='AcctTypeDesc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    schedulebillno = models.IntegerField(db_column='ScheduleBillNO', blank=True, null=True)  # Field name made lowercase.
    vat = models.BooleanField(db_column='Vat', blank=True, null=True)  # Field name made lowercase.
    applicationdate = models.DateTimeField(db_column='ApplicationDate', blank=True, null=True)  # Field name made lowercase.
    placeofwork = models.CharField(db_column='PlaceOfWork', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addressoforganisation = models.CharField(db_column='AddressOfOrganisation', max_length=40, blank=True, null=True)  # Field name made lowercase.
    giscoordinate = models.CharField(db_column='GIScoordinate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    guarantorname = models.CharField(db_column='GuarantorName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    guarantoraddress = models.CharField(db_column='GuarantorAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    organisationcode = models.CharField(db_column='OrganisationCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    institutioncode = models.CharField(db_column='institutionCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    setupdate = models.DateTimeField(db_column='SetUpDate', blank=True, null=True)  # Field name made lowercase.
    connectdate = models.DateTimeField(db_column='ConnectDate', blank=True, null=True)  # Field name made lowercase.
    distributionstation = models.CharField(db_column='DistributionStation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    injectionstation = models.CharField(db_column='InjectionStation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    upriserno = models.IntegerField(db_column='UpriserNo', blank=True, null=True)  # Field name made lowercase.
    utid = models.CharField(db_column='UTID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    buid = models.CharField(db_column='BUID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transid = models.CharField(db_column='TransID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    operatorname = models.CharField(db_column='OperatorName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=40, blank=True, null=True)  # Field name made lowercase.
    statuscode = models.CharField(db_column='StatusCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    adc = models.IntegerField(db_column='ADC', blank=True, null=True)  # Field name made lowercase.
    storedaverage = models.DecimalField(db_column='StoredAverage', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    connectiontype = models.CharField(db_column='ConnectionType', max_length=7, blank=True, null=True)  # Field name made lowercase.
    useadc = models.BooleanField(db_column='UseADC', blank=True, null=True)  # Field name made lowercase.
    isbulk = models.BooleanField(db_column='IsBulk', blank=True, null=True)  # Field name made lowercase.
    distributionid = models.CharField(db_column='DistributionID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    newsetupdate = models.DateTimeField(db_column='NewsetupDate', blank=True, null=True)  # Field name made lowercase.
    rowguid = models.CharField(max_length=36, blank=True, null=True)
    iscapmi = models.BooleanField(db_column='IsCAPMI', blank=True, null=True)  # Field name made lowercase.
    operatoredits = models.CharField(db_column='OperatorEdits', max_length=20, blank=True, null=True)  # Field name made lowercase.
    operatoredit = models.CharField(db_column='OperatorEdit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isconfirmed = models.BooleanField(db_column='IsConfirmed', blank=True, null=True)  # Field name made lowercase.
    confirmby = models.CharField(db_column='ConfirmBy', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateconfirm = models.DateTimeField(db_column='DateConfirm', blank=True, null=True)  # Field name made lowercase.
    nac = models.CharField(db_column='NAC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    backbalance = models.DecimalField(db_column='BackBalance', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    gis = models.CharField(db_column='GIS', max_length=30, blank=True, null=True)  # Field name made lowercase.
    customerid = models.CharField(db_column='CustomerID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    accounttype = models.CharField(db_column='AccountType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    newtariffcode = models.CharField(db_column='NewTariffCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dss_id = models.CharField(db_column='DSS_ID', max_length=150, blank=True, null=True)  # Field name made lowercase.
    servicecenter = models.CharField(db_column='ServiceCenter', max_length=200, blank=True, null=True)  # Field name made lowercase.
    updated_at = models.DateTimeField(auto_now=True)
    kyc = models.CharField(db_column='KYC', max_length=3, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    building_description = models.CharField(db_column='Building_Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lga = models.CharField(db_column='LGA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    premise_type = models.CharField(db_column='Premise_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customer_type = models.CharField(db_column='Customer_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # accounttype = models.CharField(db_column='Account_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    business_type = models.CharField(db_column='Business_Type', max_length=100, blank=True, null=True)  # Field name made lowercase.
    feeder_name = models.CharField(db_column='Feeder_Name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    service_band = models.CharField(db_column='Service_Band', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contactphone = models.CharField(db_column='ContactPhone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contactemail = models.CharField(db_column='ContactEmail', max_length=60, blank=True, null=True)  # Field name made lowercase.
    landlord_name = models.CharField(db_column='Landlord_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    landlord_phone = models.CharField(db_column='Landlord_Phone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tenant = models.CharField(db_column='Tenant', max_length=50, blank=True, null=True)  # Field name made lowercase.
    landlord = models.CharField(db_column='Landlord', max_length=50, blank=True, null=True)  # Field name made lowercase.
    injection_sub_station = models.CharField(db_column='Injection_Sub_Station', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cin = models.CharField(db_column='CIN', max_length=300, blank=True, null=True)  # Field name made lowercase.
    meteroem = models.CharField(db_column='MeterOEM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    upriserid = models.CharField(db_column='UpriserID', max_length=300, blank=True, null=True)  # Field name made lowercase.
    feederid = models.CharField(db_column='FeederID', max_length=300, blank=True, null=True)  # Field name made lowercase.
    ltpoleid = models.CharField(db_column='LTPoleID', max_length=300, blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(db_column='Latitude', max_length=30, blank=True, null=True)  # Field name made lowercase.
    longitude = models.CharField(db_column='Longitude', max_length=30, blank=True, null=True)  # Field name made lowercase.
    customersk = models.IntegerField(db_column='CustomerSK', blank=True, null=True)  # Field name made lowercase.
    account_nos = models.CharField( max_length=20,blank=True, null=True)  # Field name made lowercase.
    dss_name = models.CharField(db_column='DSS_Name', max_length=300, blank=True, null=True)  # Field name made lowercase.
    dss_owner = models.CharField(db_column='DSS_Owner', max_length=300, blank=True, null=True)  # Field name made lowercase.
    feeder_name = models.CharField(db_column='FeederName', max_length=300, blank=True, null=True)  # Field name made lowercase.
    feeder_type = models.CharField(db_column='FeederType', max_length=300, blank=True, null=True)  # Field name made lowercase.
    cms_created = models.BooleanField(db_column='CMS_Created', blank=True, null=True,default=False)  # Field name made lowercase.
    customer_created_by = models.CharField(db_column='Customer_Created_By', max_length=400, blank=True, null=True, default='')  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'ems_customers_new'
        
class EmsTariff(models.Model):
    tariffid = models.DecimalField(db_column='TariffID', primary_key=True, max_digits=20, decimal_places=0,default=0)  # Field name made lowercase.
    tariffcode = models.CharField(db_column='TariffCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    accounttype = models.CharField(db_column='AccountType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addeddate = models.DateTimeField(db_column='AddedDate', blank=True, null=True)  # Field name made lowercase.
    storedaverage = models.IntegerField(db_column='StoredAverage', blank=True, null=True)  # Field name made lowercase.
    ismd = models.BooleanField(db_column='isMD', blank=True, null=True)  # Field name made lowercase.
    usageratio = models.DecimalField(max_digits=50, decimal_places=1, blank=True, null=True)
    rowguid = models.CharField(max_length=360, blank=True, null=True)
    newtariffcode = models.CharField(db_column='NewTariffCode', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ems_tariff'