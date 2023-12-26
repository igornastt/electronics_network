from rest_framework import permissions


class IsUserActive(permissions.BasePermission):
    message = 'Только для активных сотрудников'

    def has_permission(self, request, view):
        if request.user.is_active:
            return True
        return False


class IsStaffOrSuperuser(permissions.BasePermission):
    message = "Вы не можете работать с объектами User!"

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False