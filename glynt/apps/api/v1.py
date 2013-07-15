# coding: utf-8
from tastypie.resources import ALL
from tastypie.api import Api
from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from glynt.apps.api import BaseApiModelResource

from django.contrib.auth.models import User

from cities_light.models import City, Country, Region

from glynt.apps.lawyer.models import Lawyer

from glynt.apps.firm.models import Firm
from glynt.apps.company.models import Company

from glynt.apps.project.models import Project
from glynt.apps.project import PROJECT_STATUS

from glynt.apps.todo.api import UserToDoCountResource

from glynt.apps.company.bunches import CompanyProfileBunch


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


class FirmSimpleResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Firm.objects.all()
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'firm/lite'
        fields = ['pk', 'name']
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()


class CompanyLiteSimpleResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Company.objects.all()
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'company/lite'
        fields = ['pk', 'name', 'website']
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        name = bundle.data.get('name', None)
        website = bundle.data.get('website', None)
        bundle.data.pop('name')
        bundle.data.pop('website')
        bundle.data.update({'name': '%s, %s' % (name, website,)})
        return bundle

def _company_profile(bundle):
    data = CompanyProfileBunch(startup=bundle.obj)
    data['profile_photo'] = data.photo_url if data.photo_url else bundle.obj.profile_photo
    data['username'] = bundle.obj.slug  # required to integrate with GlyntProfile object
    data['is_startup'] = True
    return data


class CompanyBasicProfileResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Company.objects.all().select_related('customers', 'customers_user')
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'company/profile'

        filtering = {
            'name': ALL,
            'slug': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        bundle.data.pop('data')
        bundle.data.update(_company_profile(bundle))
        return bundle


def customer_profile(bundle):
    data = {}
    if bundle.obj.profile.is_customer:
        profile = bundle.obj.customer_profile
        try:
            primary_company = profile.companies[0]
        except IndexError:
            primary_company = {}

        data.update({
            'profile_url': bundle.obj.customer_profile.get_absolute_url(),
            'summary': profile.summary,
            'bio': profile.bio,
            'companies': [
                {
                    'name': primary_company.name,
                    'summary': primary_company.summary,
                    'url': primary_company.website,
                    'twitter': primary_company.twitter}
            ],
        })
    return data


def _lawyer_profile(bundle):
    data = {}
    if bundle.obj.profile.is_lawyer:
        profile = bundle.obj.lawyer_profile
        data.update({
            'profile_url': bundle.obj.lawyer_profile.get_absolute_url(),
            'position': profile.position,
            'firm': profile.firm_name,
            'phone': profile.phone,
            'years_practiced': profile.years_practiced,
            'profile_status': profile.profile_status,
            'summary': profile.summary,
            #'fee_packages': profile.fee_packages.items(),
            'practice_locations': profile.practice_locations(),
        })
    return data


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
        bundle.data.update(customer_profile(bundle))
        return bundle


class LawyerResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get', 'put', 'patch']
        queryset = Lawyer.objects.all().prefetch_related('user', 'firm_lawyers')
        resource_name = 'lawyers'
        excludes = ['data', 'summary', 'bio']

    def dehydrate(self, bundle):
        bundle.data.pop('role')
        bundle.data['name'] = bundle.obj.user.get_full_name()
        bundle.data['position'] = bundle.obj.position
        return bundle


class ProjectResource(BaseApiModelResource):
    lawyer_id = fields.IntegerField('lawyer_id')

    class Meta(BaseApiModelResource.Meta):
        authentication = Authentication()
        authorization = UserLoggedInAuthorization()
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
            'status': PROJECT_STATUS.get_desc_by_value(bundle.obj.project_status).lower(),
        })
        return bundle


""" Register the api resources """
V1_INTERNAL_API.register(LocationSimpleResource())
V1_INTERNAL_API.register(StateSimpleResource())

V1_INTERNAL_API.register(FirmSimpleResource())
V1_INTERNAL_API.register(CompanyLiteSimpleResource())

V1_INTERNAL_API.register(UserBasicProfileResource())
V1_INTERNAL_API.register(CompanyBasicProfileResource())

V1_INTERNAL_API.register(UserToDoCountResource())

V1_INTERNAL_API.register(LawyerResource())

V1_INTERNAL_API.register(ProjectResource())
