from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class CounselorPermission(BasePermission):
    role=['counselor','manager']
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            raise  PermissionDenied("you forget to set the token in header")
        if user.role in self.role:
            if user.accept==False:
                raise PermissionDenied("manager either have not accepted you yet or just rejected you . you dont have permission")
            return True
        raise PermissionDenied("Please Provide a Valid(Counselor) Token ")
    def has_object_permission(self, request, view, obj):
        self.message = "This Counselor has no permission to delete the appointment"
        if obj:
            return request.user.id== obj.Counselor.id
        return False