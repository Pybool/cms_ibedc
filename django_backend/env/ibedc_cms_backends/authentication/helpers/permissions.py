from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from authentication.models import User, UserprocessHierarchy
from usergroups.models import AuthGroup

class Permissions():

    
    def checkDeveloperPermissions(user):
        return True

    def checkPermissions(user,code):
        positions = []
        cust_cu = UserprocessHierarchy.objects.filter(process_code =code ).values() 
        print(cust_cu)
        for pos in cust_cu:
            positions.append(pos.get('position_code'))
        print("\n\nCreate Customer Permissions ", user.can_create_customer ,  user.position in positions)
        if code == 'CUST-CU':
            return user.can_create_customer == True or (user.position in positions) == True
        elif code == 'CUST-KYC':
            return user.can_approve == True or (user.position in positions) == True
        elif code == 'CAAD':
            return user.can_approve_caad == True or (user.position in positions) == True
        else:
            return 
        
    def user_in_groups(user_mail,group_name):
        user = User.objects.get(email=user_mail)
        group = AuthGroup.objects.get(name=group_name)
        if user.groups.filter(name=group.name).exists():
            return True
        return False
    
    
    
#     from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.models import Group
# from authentication.models import User, UserprocessHierarchy
# from usergroups.models import AuthGroup, AuthenticationUserGroups

# class Permissions():

#     @staticmethod
#     @user_passes_test(lambda u: u.groups.filter(name='DEVOPS').exists() or u.is_superuser)
#     def checkDeveloperPermissions(user):
#         return True

#     def checkPermissions(user,code):
#         positions = []
#         cust_cu = UserprocessHierarchy.objects.filter(process_code =code ).values() 
#         print(cust_cu)
#         for pos in cust_cu:
#             positions.append(pos.get('position_code'))
#         print("\n\nCreate Customer Permissions ", user.can_create_customer ,  user.position in positions)
#         if code == 'CUST-CU':
#             return user.can_create_customer == True or (user.position in positions) == True
#         elif code == 'CUST-KYC':
#             return user.can_approve == True or (user.position in positions) == True
#         elif code == 'CAAD':
#             return user.can_approve_caad == True or (user.position in positions) == True
#         else:
#             return 
        
#     def user_in_groups(user_mail,group_name):
#         user = User.objects.get(email=user_mail)
#         group = AuthGroup.objects.get(name=group_name)
#         print(group)
#         if AuthenticationUserGroups.objects.filter(user=user.id,group=group.id).exists():
#             print(dir(user))
#             return True
#         return False

