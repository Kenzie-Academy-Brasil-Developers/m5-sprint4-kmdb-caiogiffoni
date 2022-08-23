from accounts.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions


class IsAdminOrCritic(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
            or request.user
            and request.user.is_critic
        )


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.critic_id or bool(
            request.user and request.user.is_superuser
        )
