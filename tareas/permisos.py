from rest_framework.permissions import BasePermission


class EsPropietarioDeLaTarea(BasePermission):
    message = "No tienes permiso para acceder a esta tarea."

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "usuario_id", None) == getattr(request.user, "id", None)