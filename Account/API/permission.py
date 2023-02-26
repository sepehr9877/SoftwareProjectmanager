from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission,IsAdminUser
from Account.models import CustomUser
from rest_framework import permissions
class RolePermission(BasePermission):
    message="You dont have role permission for this action"
    allowroles=['manager']
    def has_object_permission(self,request, view, obj):
        if request.user.is_anonymous :
            return False
        user=CustomUser.objects.filter(id=request.user.id).first()
        if request.method in permissions.SAFE_METHODS:
            if user.role in self.allowroles:
                return True
            else:
                return request.user.id == obj.first().id
        else:
            if obj is None:
                self.message="Please Provide Email Address on request parameter"
                return False
            return request.user.id == obj.first().id


class PasswordEmailPermission(BasePermission):
    message="Token is not valid"
    def has_permission(self, request, view):

        if request.user:
            return True

