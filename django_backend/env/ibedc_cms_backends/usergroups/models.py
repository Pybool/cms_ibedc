from django.db import models
from authentication.models import User,AuthGroup

# Create your models here.

        
class AuthenticationUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authentication_user_groups'
        unique_together = (('user', 'group'),)