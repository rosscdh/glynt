# coding: utf-8
from tastypie.resources import ALL
from tastypie.cache import SimpleCache
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from glynt.apps.api.models import BaseApiModelResource


from glynt.apps.company.models import Company

from glynt.apps.company.bunches import CompanyProfileBunch


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
        bundle.data.update({'name': '{name}'.format(name= website if website is not None else name)})
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


class CompanyDataBagResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Company.objects.all().select_related('customers', 'customers_user')
        authorization = Authorization()
        list_allowed_methods = ['get', 'put', 'patch']
        resource_name = 'company/data'
        fields = ['data']

        filtering = {
            'pk': ALL,
            'slug': ALL,
        }

    def dehydrate_data(self, bundle):
        return bundle.obj.data
