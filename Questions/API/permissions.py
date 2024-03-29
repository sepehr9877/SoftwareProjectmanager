from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class CheckPermissionSelfAssessment(BasePermission):
    message="Token Invalid "
    def has_permission(self, request, view):
        user=request.user
        if user.is_anonymous:
            return False
        if user.role=="patient":
            if user.accept==False:
                raise PermissionDenied("you no longer have permission as patient")
            return True
        else:
            return False
class CheckPermissionGetSelfAssessment(BasePermission):
    message="Token Invalid "
    roles=['doctor','counselor','manger']
    def has_permission(self, request, view):
        user=request.user
        if user.is_anonymous:
            return False
        if user.role in self.roles:
            if user.accept==False:
                raise PermissionDenied("manager either have not accepted you yet or just rejected you . you dont have permission")
            return True
        else:
            return False
    def has_object_permission(self, request, view, obj):
        if obj is None:
            self.message="You need to send Patient email with request params"
            return False
        return True