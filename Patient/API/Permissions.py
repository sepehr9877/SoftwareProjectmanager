from rest_framework.permissions import BasePermission


class PatientBasePermission(BasePermission):
    role=['patient']
    def has_permission(self, request, view):
        user = request.user
        if request.user.is_anonymous:
            return False
        if user.role in self.role:
            return True
        else:
            return False