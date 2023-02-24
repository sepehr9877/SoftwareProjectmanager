from rest_framework.permissions import BasePermission

class CounselorPermission(BasePermission):
    role=['counselor','manager']
    message="Please Provide a Valid Token "
    def has_permission(self, request, view):
        user = request.user
        if user.role in self.role:
            return True
        return False