from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user) and request.user.is_staff
