from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class ManagerPermission(BasePermission):
    role=['manager']
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            raise PermissionDenied("you forget to set the token in header")
        if user.role in self.role:
            return True
        raise PermissionDenied("Please Provide a Valid(Manager) Token ")
