from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GroupSerializer
# from .models import Group, User
from django.contrib.auth.models import Group
from authentication.models import User


class GroupUtils(object):
    
    def __new__(self,kw):
        self.user = kw.get('user')
        self.groups = kw.get('groups')
        if len(self.groups) < 0:
            return False
        self.user_obj = User.objects.get(email=self.user)
        self.group_obj = Group.objects.get(id=int(self.groups[0]))
        
        return self
        
    def add_user_to_group(self):
        self.group_obj.user_set.add(self.user_obj)
        
    def remove_user_from_group(self):
        self.group_obj.user_set.remove(self.user_obj)
        
    def multi_add_user_to_group(self):
        self.group_obj.user_set.add(self.user_obj)
        
    def multi_remove_user_from_group(self):
        self.group_obj.user_set.remove(self.user_obj)

class GroupView(APIView):
    
    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
