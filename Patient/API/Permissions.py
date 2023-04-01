from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class PatientBasePermission(BasePermission):
    role=['patient']
    def has_permission(self, request, view):
        user = request.user
        if request.user.is_anonymous:
            return False
        if user.role in self.role:
            if user.accept==False:
                raise PermissionDenied("manager has rejected you , you no longer have any permission as patient")
            return True
        else:
            return False