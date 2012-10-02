from django.conf import settings
from django.contrib.sites.models import Site
from django import template
import time
import ast

register = template.Library()


@register.simple_tag
def current_date_format():
    return settings.DATE_FORMAT
current_date_format.is_safe = True


@register.simple_tag
def current_site_domain():
    site = Site.objects.get_current()
    return site.domain
current_site_domain.is_safe = True


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
  if type(date_object) == str:
    date_object = time.strptime(date_object)

  return {
    'unix_timestamp': date_object.strftime("%s"),
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