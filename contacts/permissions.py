from rest_framework import permissions
from .models import User, Contact, Skill

class ContactPermission(permissions.BasePermission):
    """
    Custom permission to only allow contact owners or admin to update or remove contact.
    """
    def has_object_permission(self, request, view, obj):
        # raise Exception(request.method + " " + str(request.user.is_staff))
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:  # get, options, head
            return True
        else:
            return obj.owner == request.user

class SkillPermission(permissions.BasePermission):
    """
    Custom permission to only allow contact owners or admin to update or remove contact.
    """
    def has_permission(self, request, view):
        if request.method == "DELETE" and not request.user.is_staff:
            return False
        else:
            return True
            