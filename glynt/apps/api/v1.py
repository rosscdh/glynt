# coding: utf-8
from tastypie.resources import ALL
from tastypie.api import Api
from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from glynt.apps.api import BaseApiModelResource

from django.contrib.auth.models import User

from cities_light.models import (City, Country, Region)

from glynt.apps.lawyer.api import (_lawyer_profile, LawyerResource)

from glynt.apps.firm.api import FirmSimpleResource

from glynt.apps.customer.api import _customer_profile

from glynt.apps.company.api import (CompanyLiteSimpleResource,
                                    CompanyBasicProfileResource, CompanyDataBagResource)

from glynt.apps.project.api import (ProjectResource, 
                                    ProjectDataBagResource)

from glynt.apps.todo.api import (UserToDoCountResource, AttachmentResource, 
                                ToDoResource, FeedbackRequestResource)

V1_INTERNAL_API = Api(api_name='v1')


class UserLoggedInAuthorization(Authorization):
    """
    authorized_read_list is deprecated so made a custom Authorization class
    """
    def read_list(self, object_list, bundle):
        if not bundle.request.user.is_authenticated():
            return []
        else:
            return object_list.filter(customer=bundle.request.user.customer_profile)


class LocationSimpleResource(BaseApiModelResource):
    name = fields.CharField(attribute='name', null=True)
    region = fields.CharField(attribute='region__name', null=True)

    class Meta(BaseApiModelResource.Meta):
        queryset = City.objects.prefetch_related('region').all()
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'location/lite'
        fields = ['name', 'region']
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        name = bundle.data.get('name', None)
        region = bundle.data.get('region', None)
        bundle.data.pop('name')
        bundle.data.pop('region')
        bundle.data.update({'name': '%s, %s' % (name, region)})
        return bundle


class StateSimpleResource(BaseApiModelResource):
    name = fields.CharField(attribute='display_name', null=True)

    class Meta(BaseApiModelResource.Meta):
        # Only filter by USA, allow freeform for others
        queryset = Region.objects.filter(country_id=Country.objects.get(code3='USA'))
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'state/lite'
        fields = ['display_name', ]
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()


class UserResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        # Only filter by USA, allow freeform for others
        queryset = User.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        resource_name = 'user'
        filtering = {
            'username': ALL,
        }
        cache = SimpleCache()


class UserBasicProfileResource(BaseApiModelResource):
    name = fields.CharField(attribute='get_full_name', null=True)

    class Meta(BaseApiModelResource.Meta):
        # Only filter by USA, allow freeform for others
        queryset = User.objects.select_related('profile').filter(is_active=True)
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'user/profile'
        fields = ['pk', 'username', 'is_active', 'last_login']
        filtering = {
            'username': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data.update({
            'is_lawyer': bundle.obj.profile.is_lawyer,
            'is_customer': bundle.obj.profile.is_customer,
            'profile_photo': bundle.obj.profile.get_mugshot_url(),
            'profile_url': None,
        })
        bundle.data.update(_lawyer_profile(bundle))
        bundle.data.update(_customer_profile(bundle))
        return bundle


""" Register the api resources """
V1_INTERNAL_API.register(UserResource())
V1_INTERNAL_API.register(LocationSimpleResource())
V1_INTERNAL_API.register(StateSimpleResource())
V1_INTERNAL_API.register(FirmSimpleResource())
V1_INTERNAL_API.register(UserBasicProfileResource())
V1_INTERNAL_API.register(CompanyLiteSimpleResource())
V1_INTERNAL_API.register(CompanyBasicProfileResource())
V1_INTERNAL_API.register(CompanyDataBagResource())
V1_INTERNAL_API.register(ProjectDataBagResource())
V1_INTERNAL_API.register(UserToDoCountResource())
V1_INTERNAL_API.register(AttachmentResource())
V1_INTERNAL_API.register(ToDoResource())
V1_INTERNAL_API.register(FeedbackRequestResource())
V1_INTERNAL_API.register(LawyerResource())
V1_INTERNAL_API.register(ProjectResource())
