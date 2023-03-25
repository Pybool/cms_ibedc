from django.db import models
from authentication.models import User

# Create your models here.
class UserTasksInbox(models.Model):
    user = models.ForeignKey(User, related_name='usertasks', on_delete=models.CASCADE)
    taskid = models.CharField(max_length=255)
    task_description = models.CharField(max_length=1000)
    task_sentby = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='Created Date', null=True, blank=True)
    created_by = models.CharField(max_length=255, verbose_name='Created By', null=True, blank=True)
    edited_date = models.DateTimeField(auto_now_add=True,verbose_name='Edited Date', null=True, blank=True)
    completed_date = models.DateTimeField(verbose_name='Completed Date', null=True, blank=True)
    associated_customer = models.CharField(max_length=255, null=True, blank=True)