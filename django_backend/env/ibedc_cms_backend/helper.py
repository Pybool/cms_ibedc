from django.shortcuts import get_object_or_404

from authentication.models import User

class DotAccessibleDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value

def generate_slug(value):
    return value.replace(" ",'-').lower()

def get_user_position_code(position):
    return position.split('(')[1].split(')')[0]

def get_field_name(permission_hierarchy):
    mapping = {
        'head-quarters': '',
        'region': 'state',
        'business-unit': 'buid',
        'service-center': 'servicecenter',
    }
    return mapping.get(permission_hierarchy, None)

def get_permission_hierarchy(request):
    
    permission_hierarchy = generate_slug(request.user.permission_hierarchy)
    print("User hierarchy ===> ", permission_hierarchy)
    user = get_object_or_404(User, email=request.user.email)
    field_name = get_field_name(permission_hierarchy)
    location = permission_hierarchy.replace('-', '_')    
    if permission_hierarchy == generate_slug(user.permission_hierarchy):
        if location == 'head_quarters':
            return None, 'HQ'
        return field_name, getattr(user, location)