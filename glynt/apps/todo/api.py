# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User

from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ALL

from glynt.apps.api.models import BaseApiModelResource
from glynt.apps.todo.models import ToDo, Attachment, FeedbackRequest

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
    project = fields.IntegerField(attribute='project_id')

    class Meta(BaseApiModelResource.Meta):
        queryset = ToDo.objects.all()
        authorization = Authorization()
        resource_name = 'todo'
        list_allowed_methods = ['get', 'put', 'patch', 'post']
        #fields = ['is_deleted']
        filtering = {
            'slug': ['exact'],
            'is_deleted': ['exact'],
            'project': ['exact'],
        }

    def dehydrate(self, bundle):
        # Add display_status to the bundled object
        bundle.data['display_status'] = bundle.obj.display_status
        return bundle


class AttachmentResource(BaseApiModelResource):
    """ Api resource for creating or modifying attachments """
    project = fields.IntegerField(attribute='project_id')
    todo = fields.IntegerField(attribute='todo_id')
    uploaded_by = fields.ToOneField('glynt.apps.api.v1.UserResource', 'uploaded_by')
    deleted_by = fields.ToOneField('glynt.apps.api.v1.UserResource', 'deleted_by', null=True)

    class Meta(BaseApiModelResource.Meta):
        queryset = Attachment.objects.all()
        authentication = Authentication()
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


class FeedbackRequestResource(BaseApiModelResource):
    """ Api resource for creating or modifying feedback_requests """
    attachment = fields.ToOneField('glynt.apps.todo.api.AttachmentResource', 'attachment')
    assigned_by = fields.ToOneField('glynt.apps.api.v1.UserResource', 'assigned_by')
    assigned_to = fields.ToManyField('glynt.apps.api.v1.UserResource', 'assigned_to')

    class Meta(BaseApiModelResource.Meta):
        queryset = FeedbackRequest.objects.all()
        authorization = Authorization()
        resource_name = 'feedback_request'
        list_allowed_methods = ['get', 'post', 'patch']
        fields = []
