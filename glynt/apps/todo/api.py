# coding: utf-8
from django.contrib.auth.models import User

from glynt.apps.api import BaseApiModelResource

from glynt.apps.todo.models import ToDo


class UserToDoCountResource(BaseApiModelResource):
    """ Api resource for accessing a users todo/checklist counts """
    class Meta(BaseApiModelResource.Meta):
        queryset = User.objects.all()
        resource_name = 'todo/count'
        list_allowed_methods = ['get']
        fields = ['id', 'username', 'first_name', 'last_name', 'get_full_name']

    def get_object_list(self, request):
        return super(UserToDoCountResource, self).get_object_list(request).filter(pk=request.user.pk)

    def dehydrate(self, bundle):
        user_pk = bundle.data.pop('id')

        bundle.data.update({
            'counts': {
                'new': ToDo.objects.new(user=user_pk).count(),
                'open': ToDo.objects.open(user=user_pk).count(),
                'closed': ToDo.objects.closed(user=user_pk).count(),
            }
        })
        return bundle


class UserToDoLabelResource(BaseApiModelResource):
    """ Api resource for creating or modifying todo item names """
    class Meta(BaseApiModelResource.Meta):
        queryset = User.objects.all()
        resource_name = 'todo/name'
        list_allowed_methods = ['put']
        fields = ['name']