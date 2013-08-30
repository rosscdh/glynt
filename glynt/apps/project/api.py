# coding: utf-8
from tastypie import fields
from tastypie.resources import ALL
from tastypie.authorization import Authorization

from glynt.apps.api.models import BaseApiModelResource

from .models import Project, ProjectLawyer
from . import PROJECT_STATUS


class ProjectResource(BaseApiModelResource):
    lawyer_id = fields.IntegerField('lawyer_id')

    class Meta(BaseApiModelResource.Meta):
        queryset = Project.objects.all()
        resource_name = 'project'
        fields = ['lawyer_id', 'project_status']
        include_resource_uri = False
        include_absolute_url = True
        filtering = {
            'project_status': ALL,
        }

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

    # def dehydrate(self, bundle):
    #     bundle.data.update({
    #         'status': PROJECT_STATUS.get_desc_by_value(bundle.obj.display_status).lower(),
    #     })
    #     return bundle