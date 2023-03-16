from django.db import models
from authentication.models import User

# Create your models here.
class LocationsPermissions(models.Model):
    region = models.CharField(max_length=250, blank=True, null=True)
    biz_hub = models.CharField(max_length=250, blank=True, null=True)
    servicecenter = models.CharField(max_length=250, blank=True, null=True)
    create_uid = models.ForeignKey(User, models.DO_NOTHING, related_name="locations_cuid", db_column='create_uid', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='write_uid', related_name="locations_wid", blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=250, blank=True, null=True)
    updated_by = models.CharField(max_length=250, blank=True, null=True)
    rid = models.CharField(max_length=250, blank=True, null=True)
    buid = models.CharField(max_length=250, blank=True, null=True)
    scid = models.CharField(max_length=250, blank=True, null=True)
    service_center_address = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_locationpermissions'