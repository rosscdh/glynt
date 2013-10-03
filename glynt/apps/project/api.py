# -*- coding: UTF-8 -*-
from django.conf.urls import url

from tastypie import fields
from tastypie.resources import ALL
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash

from glynt.apps.api.models import BaseApiModelResource

from .models import Project, ProjectLawyer
from . import PROJECT_STATUS
from . import PROJECT_CATEGORY_SORT_UPDATED

import json


class ProjectResource(BaseApiModelResource):
    lawyer_id = fields.IntegerField('lawyer_id')

    class Meta(BaseApiModelResource.Meta):
        queryset = Project.objects.all()
        resource_name = 'project'
        detail_uri_name = 'uuid'
        fields = ['lawyer_id', 'project_status']
        include_resource_uri = False
        include_absolute_url = True
        filtering = {
            'project_status': ALL,
        }

    def base_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/set/(?P<%s_list>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('get_multiple'), name="api_get_multiple"),
            # url(r"^(?P<resource_name>%s)/(?P<%s>.+?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def prepend_urls(self):
        return [
            url(r"^project/$", self.wrap_view('dispatch_detail'), name='project'),
        ]

    def dehydrate(self, bundle):
        bundle.data.update({
            'status': PROJECT_STATUS.get_desc_by_value(bundle.obj.display_status).lower(),
        })
        return bundle


class ProjectDataBagResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Project.objects.all().select_related('customer', 'company', 'transactions', 'lawyers')
        authorization = Authorization()
        list_allowed_methods = ['get', 'put', 'patch']
        resource_name = 'project/data'
        fields = ['data']

        filtering = {
            'pk': ALL,
            'uuid': ALL,
        }

    def dehydrate_data(self, bundle):
        return bundle.obj.data


class ProjectLawyerResource(BaseApiModelResource):
    lawyer_id = fields.IntegerField('lawyer_id')
    project_id = fields.IntegerField('project_id')

    class Meta(BaseApiModelResource.Meta):
        queryset = ProjectLawyer.objects.all()
        authorization = Authorization()
        resource_name = 'project_lawyer'
        list_allowed_methods = ['get', 'patch']
        filtering = {
            'project': ['exact'],
            'lawyer': ['exact'],
        }


class ProjectChecklistSortResource(BaseApiModelResource):
    """
    Endpoint to handle the sorting of Checklist Items
    dont get confused with the category sort calss
    ProjectChecklistCategoriesSortResource
    """
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project_checklist_sort'
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'patch']

    def prepend_urls(self):
        return [
            url(r"^project/(?P<uuid>.+)/checklist/sort/$", self.wrap_view('dispatch_detail'), name='project_checklist_sort'),
        ]

    def patch_detail(self, request, **kwargs):
        """
        PATCH request posts in a List like so
        ['JZ7GhrcRqeFHLYcH8RD6aZ', 'Ytqp4yLcRATz7RkK98FevJ', ... ]
        this list is the new order of the project checklist todo items
        we need to update our set, but only those that change
        this event will send pusher events on change
        """
        uuid = kwargs.get('uuid', None)

        json_slugs = request.read()                     # read in the submited list of slugs
        slugs = json.loads(json_slugs)                  # convert to json

        project = Project.objects.get(uuid=uuid)          # get the appropiate project @TODO can this use the tastypie method?
        qs = project.todo_set.filter(slug__in=slugs)    # get the projects todo items

        # loop over the qs and set the order
        for todo in qs:
            found_index = slugs.index(todo.slug)

            # only update if the sort_order is different
            if todo.sort_position != found_index:
                todo.sort_position = found_index
                todo.save(update_fields=['sort_position'])


class ProjectChecklistCategoriesSortResource(BaseApiModelResource):
    """
    Endpoint to handle the sorting of Checklist Categories
    """
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project_categories_sort'
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'patch']

    def prepend_urls(self):
        return [
            url(r"^project/(?P<uuid>.+)/checklist/categories/sort/$", self.wrap_view('dispatch_detail'), name='project_categories_sort'),
        ]

    def patch_detail(self, request, **kwargs):
        """
        PATCH request posts in a List like so
        ['JZ7GhrcRqeFHLYcH8RD6aZ', 'Ytqp4yLcRATz7RkK98FevJ', ... ]
        this list is the new order of the project checklist todo items
        we need to update our set, but only those that change
        this event will send pusher events on change
        """
        uuid = kwargs.get('uuid', None)

        json_cats = request.read()                       # read in the submited list of slugs
        cats = json.loads(json_cats)                     # convert to json

        project = Project.objects.get(uuid=uuid)         # get the appropiate project @TODO can this use the tastypie method?

        # only if the lists are not the same
        if project.data.get('category_order', []) != cats:
            # override the value with our passed in value
            project.data['category_order'] = cats
            project.save(update_fields=['data'])

            PROJECT_CATEGORY_SORT_UPDATED.send(sender=self, instance=project, user=request.user, categories=cats)
