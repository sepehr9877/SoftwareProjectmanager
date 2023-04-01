from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class DoctorPatientPermission(BasePermission):
    allow_roles=['doctor','manager']
    message="this url is for doctor"
    def has_permission(self, request, view):
        user=request.user
        if request.user.is_anonymous:
            return False
        if user.role in self.allow_roles:
            if user.accept==False:
                raise PermissionDenied("manager either have not accepted you yet or just rejected you . you dont have permission")
            return True
        else:
            return False
