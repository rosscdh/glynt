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
    lawyer = context.get('object', None)
    startups_advised = lawyer.data.get('startups_advised', '[]')
    startups_advised = parse_startups(json.loads(startups_advised)) if type(startups_advised) is str else parse_startups(startups_advised)

    return {
        'lawyer': lawyer,
        'user': context.get('user', None),
        'startups': startups_advised,
        'STATIC_URL': context.get('STATIC_URL', None),
    }