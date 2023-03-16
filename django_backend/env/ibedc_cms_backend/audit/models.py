from django.db import models

class Audits(models.Model):
    table_name = models.CharField(max_length=255, verbose_name='Table Name')
    record_id = models.IntegerField(verbose_name='Record ID')
    created_date = models.DateTimeField(verbose_name='Created Date')
    created_by = models.CharField(max_length=255, verbose_name='Created By')
    updated_date = models.DateTimeField(verbose_name='Updated Date')
    updated_by = models.CharField(max_length=255, verbose_name='Updated By')
    description = models.CharField(max_length=255, verbose_name='Description')

    class Meta:
        verbose_name_plural = 'Audits log'
