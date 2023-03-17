from django.db import models
from authentication.models import User


class CrmRegion(models.Model):
    name = models.CharField(max_length=50)
    other_info = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'crm_region'
        
        
class CrmBusinessHub(models.Model):
    region = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    other_info = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'crm_business_hub'
        
class CrmServiceCentre(models.Model):
    region = models.CharField(max_length=50)
    business_hub = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    other_info = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'crm_service_centre'
        

class LocationPermissions(models.Model):
    region = models.CharField(max_length=250, blank=True, null=True)
    biz_hub = models.CharField(max_length=250, blank=True, null=True)
    service_center = models.CharField(max_length=250, blank=True, null=True)
    create_uid = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    update_uid = models.ForeignKey(User, models.DO_NOTHING, related_name="update", blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=250, blank=True, null=True)
    updated_by = models.CharField(max_length=250, blank=True, null=True)
    rid = models.CharField(max_length=250, blank=True, null=True)
    buid = models.CharField(max_length=250, blank=True, null=True)
    scid = models.CharField(max_length=250, blank=True, null=True)
    service_center_address = models.CharField(max_length=250, blank=True, null=True)
    
class EmsBusinessUnit(models.Model):
    rowguid = models.CharField(max_length=36, blank=True, null=True)
    buid = models.CharField(db_column='BUID', max_length=5, blank=True, null=True)  # Field name made lowercase.
    zoneid = models.CharField(db_column='ZoneID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contactperson = models.CharField(db_column='ContactPerson', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMail', max_length=50, blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bankcode = models.CharField(max_length=10, blank=True, null=True)
    refcode = models.CharField(max_length=5, blank=True, null=True)
    bucode = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ems_business_unit'
