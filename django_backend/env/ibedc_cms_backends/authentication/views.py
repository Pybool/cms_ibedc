# (select max(create_date) from res_users_log where res_users.id = res_users_log.create_uid) as last_authentication,

import logging
import uuid

from authentication.helpers.permissions import Permissions
from location.views import PermissionsHierarchyView
from config import CACHE_CONTROL, PAGINATION_SETTINGS

from usergroups.views import GroupUtils
from cmsadmin.models import LocationsPermissions

log = logging.getLogger(__name__)
from collections import namedtuple
import datetime as dt
from locale import currency
import os,string,json
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
import random
from django.core.paginator import Paginator
from django.utils import timezone 
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework import generics
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt, uuid, json
from django.contrib.auth.hashers import make_password, check_password
# import stripe
from rest_framework.permissions import IsAuthenticated
from .models import AuthGroup, ResetPassword, User, UserJWTtokens, UserPositions
from .cms_authenticate import ( JWTAuthenticationMiddleWare, create_access_token, 
                                 create_refresh_token, decode_access_token, decode_refresh_token
                                 )
from dotenv import load_dotenv
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .helpers.auth_helpers import AuthHelpers
from usergroups.models import AuthenticationUserGroups
load_dotenv()
refresh_jwt_token_life = int(os.getenv("REFRESH_JWT_TOKEN_LIFE"))
ISSUER_NAME = os.getenv("2FA_ISSUER_NAME")
DECLINE_REASONS = ('Shady Proposal','Has Previous Scam History','I am Uninterested')

def registration_otp(request):
    
    try:
        user = ResetPassword(email=request.data.get('email'))
       
        user.otp = random.randint(100000, 999999)
        print(user.otp)
        expiry_time = timezone.now() + timezone.timedelta(minutes=10)
        log.info(str(expiry_time))
        user.otp_expires_at = expiry_time
        user.reset_password_token = get_random_string(length=32)
        user.save()
        return {'status':True,'otp': user.otp, 'reset_password_token': user.reset_password_token}
    except:
        return {'status': False, 'message': 'Invalid Email'}

User = get_user_model()



class ActivateAccount(APIView):
    
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = {}
            user['uid'] = uid
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        decoded_payload = jwt.decode(token,'settings.SECRET_KEY', algorithms=['HS256'])
        if user is not None and (uid==decoded_payload['uid']):
            results = User.objects.get(public_id=uid)
            with transaction.atomic():
                results.isVerified = True
                results.save()    
            # user.is_active = True
            # user.save()
            results = User.objects.filter(public_id=uid).values()
            return Response({"status": True, "message": 'Thank you for your email confirmation. Now you can login your account.'}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
                
                   
class AuthSignup(APIView):
    def post(self,request):
        try:
            data = request.data
            response = {}
            if data['password'] != data['password_confirm']:
                return Response({'status':False,'message':'Passwords do not match'})
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                instance = serializer.save()
                cart = Cart.objects.create(token=get_random_string(length=32))
                instance.cart_token = cart.token
                instance.save()
                response['status'] = True
                response['email'] = instance.email
                response['cart_token'] = instance.cart_token
                
                otp_response = registration_otp(request)
                mail = {"otp":otp_response['otp'],
                        "subject":"Verify email account",
                        "sender":ISSUER_NAME,
                        "recipient":instance.email}
                send_email_task.delay(mail)
                response['temporary_otp_here'] = otp_response['otp']
                return Response(response)
            else:
                data = serializer.errors
                return Response({'status': False, 'errors': data})
        except Exception as e:
            return Response({'status': False, 'errors': f"An error {str(e)} occured during registration"})


class AuthSignin(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            print(request.data)
            email = request.data['email']
            password = request.data['password']
            user = None
            try:
                # user = VerifiedUsers.objects.get(email=email).values(password)
                user = User.objects.filter(email=email).values()

            except Exception as e:
                print('Cannot Authenticate user ',e)
                res = {'error': 'Non existent user '+ str(e)}
                return Response(res)
            
            if user:
                # try:
                    encrypted_password = user.first()['password']
                    if check_password(password, encrypted_password):
                        payload = user.first()
                        payload['exp'] = dt.datetime.now() + dt.timedelta(seconds=100000)
                        self.authhelpers = AuthHelpers()
                        logged_in_user = get_object_or_404(User,email=email) #User.objects.get()
                        logged_in_user.last_login = timezone.now()
                        logged_in_user.save()
                        # print("========alt ", create_access_token(payload))
                        token = create_access_token(payload)  #self.authhelpers._generate_jwt_token(payload, 'settings.SECRET_KEY')
                        user_details = {}
                        user_details['status'] = True
                        user_details['data'] = user[0]
                        user_details['data']['token'] = token
                    
                        return Response(user_details, status=status.HTTP_200_OK)
                    else:
                        res = {'status':False,
                            'error': 'Can not authenticate unverified user or Wrong password'}
                        return Response(res, status=status.HTTP_403_FORBIDDEN)
                    
                # except Exception as e:
                #     print("Error ",e) 
            else:
                res = {'status':False,
                       'error': 'Can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(str(e))
            res = {'error': 'please provide a email and a password'}
            return Response(res)
      

class RequestOtpView(APIView):
    def post(self,request):
        instance = User.objects.filter(email=request.data.get('email')).first()
        reset_obj = ResetPassword.objects.get(email=request.data.get('email'))
        if reset_obj.email == request.data.get('email'):
            reset_obj.delete()
        if instance is not None:
            
            return Response(registration_otp(request))
        return Response({'status':False,'message':'User not found..'})


class UserFormView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        groups = Group.objects.filter().values()
        positions = UserPositions.objects.filter().values()
        business_units = {}
        servicecenters = {}
        regions = PermissionsHierarchyView.get(PermissionsHierarchyView,request,{'as_method':True,'hierarchy':'regions','q':''})
        payload = request.GET.get('data',None)
        if payload is not None:
            locs = json.loads(payload)
            business_units = PermissionsHierarchyView.get(PermissionsHierarchyView,request,{'as_method':True,'hierarchy':'business_unit','q':locs['region']})
            servicecenters = PermissionsHierarchyView.get(PermissionsHierarchyView,request,{'as_method':True,'hierarchy':'servicecenter','q':locs['business_unit'].title()})
        return Response({'status':True,'positions':positions,'groups':groups,'regions':regions.get('regions'),'business_units':business_units.get('business_units'),'servicecenters':servicecenters.get('service_centers')})

class RegistrationValidateOtpView(APIView):
    def post(self,request):
        try:
            user = ResetPassword.objects.get(email=request.data.get('email'))
            is_otp_valid = True#int(user.otp) == int(request.data.get('otp'))
            instance = User.objects.filter(email=request.data.get('email')).first()

            # if timezone.now() > user.otp_expires_at:
            #     return Response({'status': False, 'message': 'Expired token , request for new token'})
            
            if instance is not None and is_otp_valid == True:
                instance.is_verified_account = True
                instance.save()
            return Response({'status':  True if is_otp_valid else False, 'message': "OTP validated" if is_otp_valid else "Inavlid OTP"})
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Invalid reset password token'})

class ValidateOtpView(APIView):
    def data(self,request):
        try:
            user = ResetPassword.objects.get(reset_password_token=request.data.get('reset_password_token'))
            is_otp_valid = user.otp == int(request.data.get('otp'))
            return Response({'status':  True if is_otp_valid else False, 'reset_password_token': user.reset_password_token, 'message': "OTP validated" if is_otp_valid else "Inavlid OTP"})
        except:
            return Response({'status': False, 'message': 'Invalid or expired token'})

class LogoutView(APIView):
    
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        UserJWTtokens.objects.filter(token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {'status':True,'message':'Successfully logged out'}
        return response

class ForgotPasswordView(APIView):
    
    def post(self, request):
        
        reset_otp = random.randint(100000, 999999)
        reset_token = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(50))
        try:
            reset_obj = ResetPassword.objects.get(email=request.data.get('email'))
    
            if reset_obj.email == request.data.get('email'):
                reset_obj.otp = reset_otp
                reset_obj.reset_password_token = reset_token
                reset_obj.save()
                mailservicedata = {}
                mailservicedata['otp'] = reset_otp
                mailservicedata['subject'] = "Password reset mail"
                mailservicedata['sender'] = ISSUER_NAME
                mailservicedata['recipient'] = request.data['email']
                # send_password_reset_email_task.delay(mailservicedata,)
                return Response({'status':True,'message':f'Password reset otp was sent to {request.data["email"]}','temporary_otp':reset_otp})
            else:
                return Response({'status':False,'message':f'Our database does not know you'})
        
        except Exception as e:
            log.info(str(e))
            return Response({'status':False,'message':f'Our database does not know you'})
            

class ResetPasswordView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            return Response({"status":False, "message":"Passwords do not match!"})
        reset_password_obj = ResetPassword.objects.filter(otp=data['otp']).first()
        
        if not reset_password_obj:
            return Response({"status":False, "message":"Invalid reset otp!"})
        
        user = User.objects.filter(email=reset_password_obj.email).first()
        
        if not user:
            return Response({"status":False, "message":"User not found!"})

        user.set_password(data['password'])
        user.save()
        ResetPassword.objects.filter(otp=data['otp']).delete()
        return Response({"status":True, "message":"Your password was successfully reset!"})

class ChangePassword(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def post(self,request):
        try:
            user = User.objects.get(email=request.data.get('email'), password=request.data.get('current_password'))
            user.password = user.set_password(request.data.get('new_password'))
            user.save()
            return Response({'status': True,'message':"Password has been changed"})
        except:
            return Response({'status': False, 'message': 'Invalid current password'})
  
    
class UserProfile(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    def get(self,request):
        serializer= UserShowSerializer(request.user, many=False)
        return Response({'user': serializer.data, "status": True})
    
    def put(self,request):
        if request.method == 'PUT':
            serializer= UserProfileSerializer(request.user, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                log.info(serializer.data)
                return Response({'user': serializer.data, "status": True})
            else:
                return Response({'errors': serializer.errors, "status": False})


def checkUid(uid,request):
    return False if str(request.env.user.id) != uid else True


class GetUserGroupsView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def get(self,request):
        newgroup = []
        usergroup = AuthenticationUserGroups.objects.filter(user_id=int(request.GET.get('id'))).values('group_id')
        for group in usergroup:
            newgroup.append(AuthGroup.objects.filter(id=group.get('group_id')).values('id','name').first())
        
        print(newgroup)
        return Response({"status":True,"data":newgroup})
    
class GetUsersView(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def getUsersdata(self,request):
        dev_perm = Permissions.checkDeveloperPermissions(self.request.user)
        if not dev_perm:
            if request.GET.get('id') is not None:
                users = User.objects.filter(id=int(request.GET.get('id'))).exclude(dev_perm=True).order_by('-id').values_list()
            else: 
                users = User.objects.filter().exclude(dev_perm=True).order_by('-id').values_list()
        if dev_perm:
            if request.GET.get('id') is not None:
                users = User.objects.filter(id=int(request.GET.get('id'))).order_by('-id').values_list()
            else:
                users = User.objects.filter().order_by('-id').values_list()
        return users
    
    def search_users(self,searchparam,location_type=''):

        dev_perm = Permissions.checkDeveloperPermissions(self.request.user)
        if location_type == '':
            filter = Q(name__contains=searchparam) | Q(email__contains=searchparam)
            if not dev_perm:
                users = User.objects.filter(filter).exclude(dev_perm=True).prefetch_related('groups').order_by('-id').values_list()
            if dev_perm:
                users = User.objects.filter(filter).prefetch_related('groups').order_by('-id').values_list()
                
            return users

        elif location_type in ['region','business_unit','servicecenter']:
            if location_type == 'region':
                filter = Q(region__contains = searchparam)
            elif location_type == 'business_unit':
                filter = Q(business_unit__contains = searchparam)
            elif location_type == 'servicecenter':
                filter = Q(service_center__contains = searchparam) 

            if not dev_perm:
                users = User.objects.filter(filter).exclude(dev_perm=True).prefetch_related('groups').values_list()
                
            if dev_perm:
                users = User.objects.filter(filter).prefetch_related('groups').values_list()
            return users
        
    def get(self,request,**kw):
        dev_perm = Permissions.user_in_groups(request.user.email,'DEVOPS')  #['CUST-CU','CUST-KYC','CAAD']
        create_perm = Permissions.checkPermissions(request.user,'CUST-CU')
        caad_perm = Permissions.checkPermissions(request.user,'CAAD')
        # try:
        page = request.GET.get('page', 1)
        groups = Group.objects.all().values()
        user_positions = UserPositions.objects.all().values()
        print("User positions ", user_positions)
        users=self.getUsersdata(request)  # Replace this with your own function to get users data
        
        paginator = Paginator(users, PAGINATION_SETTINGS['USERS_PER_PAGE'])
        users = paginator.get_page(page)
        serialized_users = list(users.object_list.values())
        if request.GET.get('id') is not None:
            return Response({"status":True,"data":serialized_users})
        can_manage_2fa = Permissions.user_in_groups(request.user.email,"MANAGE 2FA")
        
        print("\n\nCan manage 2fa ", can_manage_2fa,users)
        context = {
            'user_positions': user_positions,
            'groups': groups,
            'users': serialized_users,
            'dev_perm': dev_perm,
            "create_perm": create_perm,
            "caad_perm": caad_perm,
            'can_approve': Permissions.checkPermissions(request.user,'CUST-KYC'),
            'can_manage_2fa': can_manage_2fa
        }
        
        return Response({"status":True,"data":context})
        # except Exception as err:
        #     print("USers error ", err)
        
    
class SearchUsers(APIView):
    def get(self,request,**kw):
        q = request.GET.get('q', '')
        loc_type = request.GET.get('loc_type', '')
        page = request.GET.get('page', 1)
        kw = dict(request.GET.items())
        
        this = GetUsersView
        dev_perm = Permissions.checkDeveloperPermissions(self.request.user)
        create_perm = Permissions.checkPermissions(self.request.user)
        caad_perm = Permissions.checkCaadApprovalPermissions(self.request.user)
        try:
            page = int(page)
            user_groups = Group.objects.all()
            user_positions = UserPositions.objects.all()
            users=this.search_users(this,q,location_type=loc_type)
            paginator = Paginator(users, PAGINATION_SETTINGS['USERS_PER_PAGE'])
            users = paginator.get_page(page)
            can_manage_2fa = Permissions.user_in_groups(self.request.user.email,"Manage 2FA")
            context = {'user_positions':user_positions,'groups':user_groups,'users':users,'dev_perm':dev_perm,
                       "create_perm":create_perm,"caad_perm":caad_perm,"can_approve":Permissions.checkCustomerApprovalPermissions(self.request.user),"can_manage_2fa":can_manage_2fa}
            response = Response(context)
            response.headers['Cache-Control'] = CACHE_CONTROL
            return response
        except Exception as err:
            print("USers error ", err)
    
class CreateUpdateUser(APIView):
    authentication_classes = [JWTAuthenticationMiddleWare]
    
    def add_to_group(self,group_object):
        self.group_utils = GroupUtils(group_object)
        if self.group_utils is not False:
            if len(group_object.get('groups')) < 2:
                return self.group_utils.add_user_to_group(self.group_utils)
            return self.group_utils.multi_add_user_to_group(self.group_utils)

        return Response({"status":False,"message":"No group was specified for this user.."})
            
    def valsUser(self,data):
        print('Pos',data.get('position'))
        try:
            position = UserPositions.objects.get(code=data.get('position')).name
        except:
            response = {"status":False,"message":"Non existent position "}
            return Response(response)
        
        vals_user =  {
            'name': data.get('name'),
            'email': data.get('email'),
            'password': make_password(data.get('password')),
            'region':data.get('region') or 'granted',
            'business_unit':data.get('business_unit') or 'granted',
            'service_center':data.get('service_center') or data.get('servicecenter'),
            'permission_hierarchy':data.get('permission_hierarchy','Head Quarters'),
            'can_approve':data.get('can_approve',False),
            'can_create_user':data.get('can_create_user',False),
            'enable_2fa':data.get('enable_2fa',False),
            'can_create_customer':data.get('can_create_customers',False),
            'can_approve_caad':data.get('can_approve_caad',False),
            'position':position,
            'can_manage_2fa':data.get('can_manage_2fa',False),
            'administration':data.get('administration',''),
            
            }
        if data.get('buid') != None:
            vals_user['buid']=data.get('buid').upper()
        
        print(data)
        return vals_user

    def group_factory(self,newuser,user,data,vals_user,messages):
        if newuser:
            user_list = []
            user_list.append(user.id)
            groups = data.get('groups',[])
            default_groups = {'user':user.email,'groups':[Group.objects.get(name='BASE USER').id]}
            self.group_utils = GroupUtils(default_groups)
            self.group_utils.add_user_to_group(self.group_utils)
            
            if vals_user['can_manage_2fa']:
                try:
                    print("Groups ========> ", Group.objects.filter().values())
                    two_fa_groups = {'user':user.email,'groups':[Group.objects.get(name='MANAGE 2FA').id]}
                    self.add_to_group(two_fa_groups)
                except Exception as e:
                    print(str(e))
                    if "Group matching query does not exist" in str(e):
                        return {"status":False,"message":messages['GROUP_NO_EXIST']}
                        
            
            if data.get('administration') == "Ibedc Administrator":
                access_right_groups = {'user':user.email,'groups':['IBEDC ADMIN']}
                self.add_to_group(access_right_groups)
                
            
            elif data.get('administration') == "ROOT":
                access_right_groups = {'user':user.email,'groups':['ROOT']}
                self.add_to_group(access_right_groups)
            
            print("New user groups ", groups)
            if len(groups) > 0:
                for group in groups:
                    group_item = {'user':user.email,'groups':[int(group)]}
                    self.add_to_group(group_item)
            # self.assign_user_group(user_list,groups)
            return{"status":True,"data":str(newuser),"message":messages['SUCCESS']}  
        
        
    def post(self,request,**kw): #CREATE NEW USER AND ASSIGN GROUPS
        self.data = request.data
        data = self.data        
        vals_user = self.valsUser(data)
        try:
            newuser = User.objects.create(**vals_user)
            user = User.objects.get(id=newuser.id)
        except Exception as e:
            if "unique constraint" in str(e):
                response = {"status":False,"message":"User with this email already exists"}
            else:
                print(str(e))
                response = {"status":False,"message":"An error occured while creating this user"}
            return Response(response)
        messages = {'GROUP_NO_EXIST':'User was created but could not be added to Manage 2FA, Group might not exist',
                    'SUCCESS':'User was created successfully'}
        if newuser:
            return Response(self.group_factory(newuser,user,data,vals_user,messages))
        response = {"status":False,"data":str(newuser),"message":"Something went wrong while creating user"}  
        return Response(response) 
                    

    def edit_user(self,vals_user, data):
        
        try:
            user_id = int(data.get('id'))
            User.objects.filter(id=user_id).update(**vals_user)
            newuser = User.objects.get(id=user_id)
            return newuser,True #Update with password == True
        
        except Exception as e:
            print("Edit exception ",e)
            user = User.objects.filter(login=data.get('login')).values('id').first()
            if user is not None:
                user_id = user['id']
                User.objects.filter(id=user_id).update(**vals_user)
                newuser = User.objects.get(id=user_id)
            return newuser,False #Update without password == False
    
    
    def get(self,request,**kw): #RESET 2FA CREDENTIALS...
        user_id = request.GET.get('user_id')
        user_id = int(user_id)
        mass_change = Permissions.user_in_groups(self.request.user.email,"Manage 2FA")
        if not mass_change:
            response = {"status":False,"message":"You do not have permission to perform this operation"}  
            return json.dumps(response) 
            
        user =User.objects.get(id=user_id)
        user.action_discard_2f_auth_credentials()
        print(f"\n\n2FA for user {user_id} was reset...")
        response = {"status":True,"message":f"2FA for user {user.login} was reset..."}  
        return json.dumps(response)  
          
    def put(self,request,**kw): #UPDATE ALREADY CREATED USER(S)
        self.data = request.data
        data = self.data        
        vals_user = self.valsUser(data)
        print(vals_user)
        # vals_user.pop('password')
        try:
            update_user_count = User.objects.filter(id=int(data.get('id'))).update(**vals_user)
            print("Update count ===> ", update_user_count)
            if update_user_count > 0:
                user = User.objects.get(id=int(data.get('id')))
            else:
                return Response({"status":False,"message":"An error occured while updating this user"})
        except Exception as e:
            print(e)
            response = {"status":False,"message":"An error occured while updating this user"}
            return Response(response)
        messages = {'GROUP_NO_EXIST':'User was updated but could not be added to Manage 2FA, Group might not exist',
                    'SUCCESS':'User was updated successfully'}
        if user:
            return Response(self.group_factory(user,user,data,vals_user,messages))
        response = {"status":False,"data":str(user),"message":"Something went wrong while updating user"}  
        return Response(response) 
    
    def assign_user_groups(self,user_ids,group_ids):
        users_ids = user_ids # list
        aux_users = [(4, i) for i in users_ids]
        for x in range(0,len(group_ids)): 
            group = http.request.env['res.groups'].sudo().search([('id', '=', group_ids[x])])
            print("Add to Group ",group,aux_users)
            group.sudo().write({'users': aux_users})
    
    def delete_user_from_group(self,user_id,group_name):
        # group_name = http.request.env['res.groups'].sudo().search([('id', '=', group_id)])[0].name
        try:
            group_e = http.request.env['res.groups'].sudo().search([('name', '=', group_name)])
            print("group to remove from ", group_e)
            status = group_e.sudo().write({'users': [(3, user_id)]})
            print("Remove from group status ", status)
        except Exception as e:
            pass
                    
    # @http.route(['/cms/delete_user/'], website=True,auth='user')
    def delete_user(self,user_ids):
        print(user_ids)
        print("User id ", json.loads(user_ids),type(json.loads(user_ids)))
        user_ids = json.loads(user_ids)[0]['users']
        for user_id in user_ids:
            pass
            # http.request.env['res.users'].sudo().search([('id', '=', user_id)]).unlink()
            # return self.userpage()
        response = {"status":True,"message":"User(s) deleted successfully"}  
        return Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')
    
    # @http.route(['/cms/activation_users/'], website=True,auth='user')
    def deactivate_user(self,user_ids,action):
        try:
            print("\n\nUser ids and actions ",user_ids,action)
            print("User id ", json.loads(user_ids),type(json.loads(user_ids)))
            user_ids = json.loads(user_ids)[0]['users']
            vals_user = {'active': False} if int(action) == 0 else {'active': True}
            for user_id in user_ids:
                editeduser =request.env['res.users'].sudo().browse(int(user_id)) #
                editeduser.sudo().write(vals_user)
            response = {"status":True,"message":"User(s) deactivated successfully"}  if int(action) == 0 else {"status":True,"message":"User(s) activated successfully"}
            return Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')
        
        except Exception as e:
            if "You cannot deactivate the user you're currently logged in as" in str(e):
                response = {"status":False,"message":"You cannot deactivate the user you're currently logged in as"}
                return Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')
            else:
                response = {"status":False,"message":"An error occured while deactivating user"}
                return Response(json.dumps(response, default=Serializables.jsonSerializer),content_type='text/json;charset=utf-8')
        
    