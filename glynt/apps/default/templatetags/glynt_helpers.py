# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django import template

import hmac, hashlib
import time

register = template.Library()


@register.simple_tag
def current_date_format():
    return settings.DATE_FORMAT
current_date_format.is_safe = True

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def current_site_domain():
    site = Site.objects.get_current()
    return site.domain
current_site_domain.is_safe = True


@register.simple_tag
def colorize_acronym(acronym):
    color_class = None

    if acronym == 'cl':
        color_class = 'c1'
    elif acronym == 'la':
        color_class = 'c2'
    elif acronym == 'nda':
        color_class = 'c3'
    elif acronym == 'hsp':
        color_class = 'c4'
    else:
        color_class = 'c5'
    return color_class
colorize_acronym.is_safe = True


@register.inclusion_tag('document/partials/document_status.html')
def document_status(document):
  status = None
  if document.num_signed == 0 and document.num_invited == 0:
    status = 'no_invites'
  elif document.num_invited in [0,None,'']:
    status = 'no_invites'
  elif document.num_signed == document.num_invited:
    status = 'signed'
  elif document.num_signed != document.num_invited:
    status = 'out'

  return {
    'status': status,
    'num_invited': document.num_invited,
    'num_signed': document.num_signed,
    'meta': document.meta_data,
  }


@register.inclusion_tag('moment/moment.js')
def moment_js(selector=None):
  selector = '[data-humanize-date]' if selector is None else selector
  return {
    'selector': selector
  }


@register.inclusion_tag('moment/moment.html')
def moment(date_object, default_date):
    unix_timestamp = None
    if type(date_object) == str:
        date_object = time.strptime(date_object)
    if date_object:
        unix_timestamp = date_object.strftime("%s")

    return {
        'unix_timestamp': unix_timestamp,
        'default_date': default_date
    }


@register.inclusion_tag('comments/form.html')
def comment_form(form, next):
    return {
      'form': form,
      'next': next
    }


@register.inclusion_tag('pleasewait/loading.html')
def show_loading(**kwargs):
    true_eval = (True, 'True')
    false_eval = (False, 'False')
    kwargs['STATIC_URL'] = settings.STATIC_URL
    kwargs['just_image'] = True if 'just_image' in kwargs and kwargs['just_image'] in true_eval else False
    kwargs['modal'] = False if 'modal' in kwargs and kwargs['modal'] in false_eval else True
    kwargs['header'] = False if 'header' in kwargs and kwargs['header'] in false_eval else True
    kwargs['body'] = False if 'body' in kwargs and kwargs['body'] in false_eval else True
    kwargs['footer'] = False if 'footer' in kwargs and kwargs['footer'] in false_eval else True
    return kwargs


@register.inclusion_tag('vendors/intercom.html', takes_context=True)
def intercom_script(context, **kwargs):
    user = context.get('user', None)
    intercomio_userhash = None
    # were not in dev (because we dont want intercom to record us devs)
    if getattr(settings, 'PROJECT_ENVIRONMENT', None) != 'dev':
        if user and user.is_authenticated():
            intercomio_userhash = hmac.new(settings.INTERCOM_API_SECRET, str(user.pk), digestmod=hashlib.sha256).hexdigest()

    context.update({
        'intercomio_userhash': intercomio_userhash,
    })
    return context
intercom_script.is_safe = True


@register.inclusion_tag('partials/contact_us_form.html', takes_context=True)
def contact_us_form(context, modal_mode=True, **kwargs):
    context.update({
        'modal_mode': modal_mode,
    })
    return context
contact_us_form.is_safe = True