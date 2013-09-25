# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
from tastypie.resources import ALL
from tastypie.cache import SimpleCache

from glynt.apps.api.models import BaseApiModelResource

from .models import Firm


class FirmSimpleResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Firm.objects.all()
        list_allowed_methods = ['get']
        resource_name = 'firm/lite'
        fields = ['pk', 'name']
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()