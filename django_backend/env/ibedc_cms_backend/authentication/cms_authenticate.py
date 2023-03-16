from datetime import datetime
import os, jwt, datetime
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from .models import User
from dotenv import load_dotenv
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
load_dotenv()
algorithm = str(os.getenv("JWT_ALGORITHM"))
jwt_token_life = int(os.getenv("JWT_TOKEN_LIFE"))
jwt_token_secret_key = str(os.getenv("JWT_TOKEN_SECRET_KEY"))
refresh_jwt_token_life = int(os.getenv("REFRESH_JWT_TOKEN_LIFE"))

def get_authorization_token(request,auth):
        auth = get_authorization_header(request).split()
        
        if auth and len(auth)==2:
            print(auth)
            return auth[1].decode('utf-8')
        if auth is True:
            pass
            # raise exceptions.AuthenticationFailed('Unauthenticated')
        return False

def get_permissions_hierarchy(payload):
    user = get_object_or_404(User,email=payload['email'])
    hierarchy_order = {
        'state': user.is_level_user('region'),
        'buid': user.is_level_user('buid'),
        'servicecenter': user.is_level_user('servicecenter'),
        'hq': user.is_level_user('hq'),
    }
    for key, val in hierarchy_order.items():
        if val:
            key = key
            break
        
    permissions_dict = {
        'state': payload['region'],
        'buid': payload['business_unit'],
        'servicecenter': payload['service_center'],
        'bucode': payload['bucode']
    }
    return {"key":key,"permissions_dict":permissions_dict}
    
# Authentication MIDDLEWARE CLASS 
class JWTAuthenticationMiddleWare(BaseAuthentication):
        
    def authenticate(self,request,auth=True):
        
        token = get_authorization_token(request,auth)
        id = decode_access_token(token)
        user = User.objects.get(id=id)
        print(user)
        return (user, None)
           
def create_access_token(user):
    permissions = get_permissions_hierarchy(user)
    return jwt.encode({
        'id':user['id'],
        'active':user['active'],
        'action_id':user['action_id'],
        'suspend_user':user['suspend_user'],
        'permission_hierarchy':user['permission_hierarchy'],
        'region':user['region'],
        'business_unit':user['business_unit'],
        'service_center':user['service_center'],
        'can_approve':user['can_approve'],
        'bucode':user['bucode'],
        'enable_2fa':user['enable_2fa'],
        'secret_code_2fa':user['secret_code_2fa'],
        'can_manage_2fa':user['can_manage_2fa'],
        'position':user['position'],
        'can_approve_caad':user['can_approve_caad'],
        'can_create_user':user['can_create_user'],
        'can_create_customer':user['can_create_customer'],
        'is_dev':user['is_dev'],
        'email':user['email'],
        'key':permissions['key'],
        'permissions_dict':permissions['permissions_dict'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=jwt_token_life),
        'iat':datetime.datetime.utcnow()
    },jwt_token_secret_key,algorithm=algorithm)
    
def decode_access_token(token,cart=False):
    try:
        payload = jwt.decode(token,jwt_token_secret_key,algorithms=algorithm)
        return payload['id']
    except Exception as e:
        raise exceptions.AuthenticationFailed('Unauthenticated user')
        
def create_refresh_token(payload_object):
    
    return jwt.encode({
        'public_id':payload_object['public_id'],
        'username':payload_object['username'],
        'is_admin':payload_object['is_admin'],
        'is_root':payload_object['is_root'],
        'email':payload_object['email'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=refresh_jwt_token_life),
        'iat':datetime.datetime.utcnow()
    },jwt_token_secret_key,algorithm=algorithm)

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token,jwt_token_secret_key,algorithms=algorithm)
        return payload['user_id']
    except Exception as e:
        raise exceptions.AuthenticationFailed('Unauthenticated user')