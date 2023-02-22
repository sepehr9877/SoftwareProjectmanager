from rest_framework.permissions import BasePermission,IsAdminUser
from Account.models import CustomUser
from rest_framework import permissions
class RolePermission(BasePermission):
    message="You dont have role permission for this action"
    def has_object_permission(self, request, view, obj):
        print(request.user)
        if request.user.is_anonymous :
            return False
        user=CustomUser.objects.filter(id=request.user.id).first()
        if(user.role=="patient"):
            return request.user.id == obj.id
        else:
            return True


