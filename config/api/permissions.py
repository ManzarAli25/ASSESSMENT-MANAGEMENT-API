from rest_framework import permissions

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Instructors').exists()

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Students').exists()
