# -*- coding: UTF-8 -*-
from django.contrib import admin, sites

from cities_light.models import City, Country, Region
from cities_light.models import City, Country, Region
from django.contrib.sites.models import Site

admin.site.unregister(City)
admin.site.unregister(Country)
admin.site.unregister(Region)
admin.site.unregister(Site)
