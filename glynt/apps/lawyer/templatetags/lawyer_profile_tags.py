# -*- coding: utf-8 -*-
from itertools import chain
from django import template
from django.template.defaultfilters import slugify

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.startup.models import Startup

import json

register = template.Library()

def parse_startups(startups):
    startup_list = []
    for startup in startups:
        name = url = None
        try:
            name, url = startup.split(',')
            name = name.strip()
            url = url.strip()
        except ValueError:
            name = startup.strip()
        startup_list.append((unicode(slugify(name)), name, url))

    return set(list(chain(Startup.objects.filter(slug__in=[slug for slug,n,u in startup_list]) \
        , Startup.objects.filter(website__in=[url for s,n,url in startup_list]))))


@register.inclusion_tag('lawyer/partials/startups_advised.html', takes_context=True)
def startups_advised(context):
    context.update({
        'lawyer': context.get('object', None),
        'startups': lawyer.startups_advised,
    })
    return context