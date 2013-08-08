# coding: utf-8
from django.contrib.auth.models import User

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ALL

from glynt.apps.api import BaseApiModelResource
from glynt.apps.todo.models import ToDo, Attachment

import time


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
        bundle.data.pop('id')

        bundle.data.update({
            'counts': {
                # 'new': ToDo.objects.new(user=user_pk).count(),
                # 'open': ToDo.objects.open(user=user_pk).count(),
                # 'closed': ToDo.objects.closed(user=user_pk).count(),
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


class ToDoResource(BaseApiModelResource):
    """ Api resource for creating or modifying todo item names """
    class Meta(BaseApiModelResource.Meta):
        queryset = ToDo.objects.all()
        authorization = Authorization()
        resource_name = 'todo'
        list_allowed_methods = ['get', 'put', 'patch']
        #fields = ['is_deleted']
        filtering = {
            'is_deleted': ['exact'],
        }


class AttachmentResource(BaseApiModelResource):
    """ Api resource for creating or modifying attachments """
    project = fields.IntegerField(attribute='project_id')
    todo = fields.IntegerField(attribute='todo_id')

    class Meta(BaseApiModelResource.Meta):
        queryset = Attachment.objects.all()
        authorization = Authorization()
        resource_name = 'attachment'
        list_allowed_methods = ['get', 'post', 'delete']
        filtering = {
            'project': ALL,
            'todo': ALL,
        }

    def dehydrate(self, bundle):
        bundle.data.pop('data')
        bundle.data['data'] = bundle.obj.data
        bundle.data['date_created_unix'] = time.mktime(bundle.obj.date_created.timetuple())
        return bundle
