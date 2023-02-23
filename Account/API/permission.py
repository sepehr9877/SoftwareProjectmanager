from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission,IsAdminUser
from Account.models import CustomUser
from rest_framework import permissions
class RolePermission(BasePermission):
    message="You dont have role permission for this action"
    allowroles=['counselor','manager']
    def has_object_permission(self,request, view, obj):
        if request.user.is_anonymous :
            return False
        user=CustomUser.objects.filter(id=request.user.id).first()
        if obj is None:
            if user.role in self.allowroles:
                return True
            return False
        if(user.role=="patient"):
            return request.user.id == obj.first().id
        else:
            return True


class PasswordEmailPermission(BasePermission):
    message="Token is not valid"
    def has_permission(self, request, view):

        if request.user:
            return True

