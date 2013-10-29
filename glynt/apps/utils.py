# encoding: utf-8
"""
In order to provide clean access to constants used in model definitions
This class provides a simple lookup mechnism which allows static reference to named values
instead of having to hardcode the numeric variable
"""
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse

from django.db.models import Q

import re
import json
import urlparse
import shortuuid
import datetime
import random


# hardcoded here cos i havent yet figured out how to reverse tastypie urls (?)
API_URLS = {
    'locations': '/api/v1/location/lite/?format=json&limit=15',
    'states': '/api/v1/state/lite/?format=json&limit=15',
    'companies': '/api/v1/company/lite/?format=json&limit=15',
}

def CURRENT_SITE():
    return Site.objects.get(pk=settings.SITE_ID)

def generate_unique_slug(instance=None):
    """ Generate the unique slug for a model instance """
    if instance is not None:
        pk = instance.pk if hasattr(instance, 'pk') and type(instance.pk) is not None else random.random()
        hash_val = '%s-%s-%s' % (instance.__class__.__name__, pk, datetime.datetime.utcnow())
        return shortuuid.uuid(name=hash_val)
    else:
        return shortuuid.uuid()


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def _get_referer(request):
    """Return the HTTP_REFERER, if existing."""
    if 'HTTP_REFERER' in request.META:
        sr = urlparse.urlsplit(request.META['HTTP_REFERER'])
        return urlparse.urlunsplit(('', '', sr.path, sr.query, sr.fragment))

    return None


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        if self.request.is_ajax():
            errors = form.errors['__all__'] if '__all__' in form.errors else form.errors
            data = {
                'errors': errors
            }
            return self.render_to_json_response(data, status=400)
        else:
            return super(AjaxableResponseMixin, self).form_invalid(form)

    def form_valid(self, form):
        """ save the form but also render via ajax if ajax request """
        if self.request.is_ajax():
            if hasattr(form, 'instance'):
                form.instance.save()
                data = {
                    'pk': form.instance.pk,
                    'url': form.instance.get_absolute_url() if hasattr(form.instance, 'get_absolute_url') else None,
                }
                return self.render_to_json_response(data)

        return super(AjaxableResponseMixin, self).form_valid(form)


def get_namedtuple_choices(name, choices_tuple):
    """Factory function for quickly making a namedtuple suitable for use in a
    Django model as a choices attribute on a field. It will preserve order.

    Usage::

        class MyModel(models.Model):
            COLORS = get_namedtuple_choices('COLORS', (
                (0, 'BLACK', 'Black'),
                (1, 'WHITE', 'White'),
            ))
            colors = models.PositiveIntegerField(choices=COLORS)

        >>> MyModel.COLORS.BLACK
        0
        >>> MyModel.COLORS.get_choices()
        [(0, 'Black'), (1, 'White')]

        class OtherModel(models.Model):
            GRADES = get_namedtuple_choices('GRADES', (
                ('FR', 'FR', 'Freshman'),
                ('SR', 'SR', 'Senior'),
            ))
            grade = models.CharField(max_length=2, choices=GRADES)

        >>> OtherModel.GRADES.FR
        'FR'
        >>> OtherModel.GRADES.get_choices()
        [('FR', 'Freshman'), ('SR', 'Senior')]

    """
    class Choices(namedtuple(name, [name for val,name,desc in choices_tuple])):
        __slots__ = ()
        _choices = tuple([desc for val,name,desc in choices_tuple])

        def get_choices(self):
            return zip(tuple(self), self._choices)

        def get_values(self):
            values = []
            for val,name,desc in choices_tuple:
                if isinstance(val, type([])):
                    values.extend(val)
                else:
                    values.append(val)
            return values

        def get_value_by_name(self, input_name):
            for val,name,desc in choices_tuple:
                if name == input_name:
                    return val
            return False

        def get_desc_by_value(self, input_value):
            for val,name,desc in choices_tuple:
                if val == input_value:
                    return desc
            return False

        def is_valid(self, selection):
            for val,name,desc in choices_tuple:
                if val == selection or name == selection or desc == selection:
                    return True
            return False

    return Choices._make([val for val,name,desc in choices_tuple])


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect
    def removed(self):
        return self.set_past - self.intersect
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


def user_is_self_or_admin(request, viewed_user):
    """
    Decorator to ensure you can only edit your own profile
    unless you are an admin or mod
    """
    if not request.user.is_authenticated():
        messages.error(request, _('You need to be logged in.'))
        return HttpResponseRedirect( settings.LOGIN_URL )

    if request.user != viewed_user and (not request.user.is_staff and not request.user.is_superuser ):
        messages.error(request, _('You are trying to access someones profile without permission. You are a very norty person.'))
        return HttpResponseRedirect( settings.LOGIN_URL )

    return True




def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query