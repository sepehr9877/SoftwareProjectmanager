from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission,IsAdminUser
from Account.models import CustomUser
from rest_framework import permissions
class RolePermission(BasePermission):
    message="You dont have role permission for this action"
    def has_object_permission(self,request, view, obj):
        print("enter to permisio")
        if request.user.is_anonymous :
            return False
        user=CustomUser.objects.filter(id=request.user.id).first()
        if(user.role=="patient"):
            print(request.user.id == obj.id)
            return request.user.id == obj.id
        else:
            return True
class GetAllPatientsPermission(BasePermission):
    message="This is for Counselor and Manger "
    def has_permission(self, request, view):
        role=request.user.role
        allow_roles=['counselor','manager']
        if role in allow_roles:
            return True
        else:
            return False


