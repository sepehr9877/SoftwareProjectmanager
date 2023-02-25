
from rest_framework.permissions import BasePermission

class CheckPermissionSelfAssessment(BasePermission):
    message="Token Invalid "
    def has_permission(self, request, view):
        user=request.user
        if user.is_anonymous:
            return False
        if user.role=="patient":
            return True
        else:
            return False
