from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import redirect
# from dashboard import views
from django.contrib import messages
from tasks.models import UserTasksInbox


def is_caad_initiator():
    def decorator(view_func):
        def wrapper_func(self,request, *args, **kwargs):
            if not 'BHM' in request.user.position:
                msg = {'status':False,'message':'You are not authorized to initiate a caad review'}
                return Response(msg)
            return view_func(self,request, *args, **kwargs)
        return wrapper_func
    return decorator


def is_valid_caad_bha():
    def decorator(view_func):
        def wrapper_func(self,request, *args, **kwargs):
            
            if not 'BHA' in request.user.position:
                msg = {'status':False,'message':'You are not authorized to decline this caad record'}
                return Response(msg)
            else:
                try:
                    pass
                    return view_func(self,request, *args, **kwargs)
                
                    # print("Decorator args===> ",request.data.get('task_id'))
                    # print(UserTasksInbox.objects.get(taskid=request.data.get('task_id')))
                    task_owner = {}#UserTasksInbox.objects.get(taskid=request.data.get('task_id')).user
                except Exception as e:
                    print(str(e))
                    return Response({'status':False,'message':'Something went wrong , this should not have happened'})
                # if task_owner.business_unit == request.user.business_unit:
                #     return view_func(self,request, *args, **kwargs)
                # else:
                #     return Response({'status':False,'message':'You are not authorized to decline this caad record'})
        return wrapper_func
    return decorator
