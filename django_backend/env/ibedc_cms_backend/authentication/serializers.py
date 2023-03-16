from datetime import date, datetime
from decimal import Decimal
import uuid
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import User

import operator, functools
from django.db import transaction
import logging
log = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['name', 'email', 'password', 'position', 'privilegde',
              'can_create_customers','can_approve','can_approve_caad',
              'can_mange_2fa','permissions_hierarchy','enable_2fa','region',
              'business_unit','servicecenter'
              ]