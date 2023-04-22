from django.db import models

class PositionCodes(models.Model):
    name = models.CharField(max_length=255, unique=True)    
    class Meta:
        db_table = 'user_position_codes'

class AccountType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'ibedc_account_type'


class BuildingDescription(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'ibedc_building_description'


class CustomerCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'ibedc_customer_category'


class CustomerType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'ibedc_customer_type'


class PremiseType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'ibedc_premise_type'


class SupplyType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'ibedc_supply_type'


class ServiceBand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'ibedc_service_band'


class CaadVat(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'ibedc_caad_vat'

class UserProcessHierarchy(models.Model):
    process_code = models.CharField(max_length=255)
    precedence = models.IntegerField(default=0)
    position_code = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'ibedc_user_process_hierarchy'

    
    def get_processes():
        """Process codes"""
        
        processes = [   {"code":"CUST-CU","name":"Customer Creation/Update Process"},
                        {"code":"CUST-KYC","name":"Customer Kyc Approval Process"},
                        {"code":"BHM-OPC","name":"BHM & Operations Compliance"},
                        {"code":"CAAD","name":"Customer Account Adjustment Document"},
                    ]
        return processes