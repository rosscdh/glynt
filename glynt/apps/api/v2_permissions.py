# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated


class GlyntObjectPermission(IsAuthenticated):
    """
    Hook out read,edit,delete up to the django-rulez helper
    methods
    """
    def can_edit(self, request, view, obj):
        if hasattr(obj, 'can_edit'):
            return obj.can_edit(user=request.user, request=request)
        return False

    def can_delete(self, request, view, obj):
        if hasattr(obj, 'can_delete'):
            return obj.can_delete(user=request.user, request=request)
        return False

    def can_read(self, request, view, obj):
        if hasattr(obj, 'can_read'):
            return obj.can_read(user=request.user, request=request)
        return False

    def has_object_permission(self, request, view, obj):
        has_permission = False

        if request.method in ['POST', 'PUT', 'PATCH']:
            has_permission = self.can_edit(request=request, view=view, obj=obj)

        elif request.method in ['DELETE']:
            has_permission = self.can_delete(request=request, view=view, obj=obj)

        elif request.method in ['GET']:
            has_permission = self.can_read(request=request, view=view, obj=obj)


        return has_permission