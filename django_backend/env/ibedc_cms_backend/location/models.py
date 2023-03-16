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
