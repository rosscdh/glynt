# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django import template

import hmac
import hashlib
import time

register = template.Library()

import logging
logger = logging.getLogger('django.request')


@register.simple_tag
def current_date_format():
    return settings.DATE_FORMAT
current_date_format.is_safe = True


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


@register.inclusion_tag('moment/moment.js')
def moment_js(selector=None):
    selector = '[data-humanize-date]' if selector is None else selector
    return {'selector': selector}


@register.inclusion_tag('moment/moment.html')
def moment(date_object, default_date=None):
    if default_date is None:
        default_date = date_object

    unix_timestamp = None

    if type(date_object) == str:
        date_object = time.strptime(date_object)
    if date_object:
        unix_timestamp = date_object.strftime("%s")

    return {
        'unix_timestamp': unix_timestamp,
        'default_date': default_date
    }


@register.filter(takes_context=False)
def humanise_number(num):
    if not isinstance(num, ( int, long )):
        num = 0
        logger.info('Value "num" passed to humanise_number must be a number is type: %s %s' % (type(num),num,))

    magnitude = 0

    while num >= 1000:
        magnitude += 1
        num /= 1000

    humanised_num = '%s%s' % (num, ['', 'k', 'm', 'g', 't', 'p'][magnitude])
    return humanised_num


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
    show_widget = getattr(settings, 'PROJECT_ENVIRONMENT', None) != 'dev' and user.is_authenticated()
    # were not in dev (because we dont want intercom to record us devs)
    if show_widget:
        if user and user.is_authenticated():
            intercomio_userhash = hmac.new(settings.INTERCOM_API_SECRET, str(user.pk), digestmod=hashlib.sha256).hexdigest()

    context.update({
        'show_widget': show_widget,
        'intercomio_userhash': intercomio_userhash,
    })
    return context
intercom_script.is_safe = True


@register.inclusion_tag('public/partials/contact_us_wrapper.html', takes_context=True)
def contact_us_form(context, is_modal=None, **kwargs):
    is_modal = True if is_modal is None and context.get('request').is_ajax() else False
    context.update({
        'is_modal': is_modal,
    })
    return context
contact_us_form.is_safe = True


@register.inclusion_tag('public/partials/write_message_form.html', takes_context=True)
def write_message_form(context, is_modal=None, **kwargs):
    is_modal = True if is_modal is None and context.get('request').is_ajax() else False
    context.update({
        'is_modal': is_modal,
    })
    return context
write_message_form.is_safe = True

@register.inclusion_tag('partials/handlebars_messages.js', takes_context=True)
def handlebars_messages(context, **kwargs):
    output_target = kwargs.get('output_target', None)
    target_in_before_after = kwargs.get('target_in_before_after', None)

    context.update({
        'output_target': output_target if output_target else 'div.navbar.navbar-fixed-top:first',
        'target_in_before_after': target_in_before_after if target_in_before_after else 'after'
    })
    return context
handlebars_messages.is_safe = True


@register.inclusion_tag('partials/profile_card_templates.html', takes_context=True)
def profile_card_templates(context, **kwargs):
    kwargs.update({
        'DEBUG': settings.DEBUG
    })
    context.update(kwargs)
    return context
profile_card_templates.is_safe = True


@register.inclusion_tag('partials/profile_cards.js', takes_context=False)
def profile_card_js(**kwargs):
    context = {}
    kwargs.update({
        'DEBUG': settings.DEBUG
    })
    context.update(kwargs)
    return context
profile_card_js.is_safe = True


@register.inclusion_tag('comments/comments.js')
def comments_js():
    return {}


@register.filter
def as_percentage_of(part, whole):
    part = (int(part))
    whole = (int(whole))
    try:
        return "%d%%" % (float(part) / float(whole) * 100)
    except (ValueError, ZeroDivisionError):
        return ""