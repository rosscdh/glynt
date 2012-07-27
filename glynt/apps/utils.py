# encoding: utf-8
"""
In order to provide clean access to constants used in model definitions
This class provides a simple lookup mechnism which allows static reference to named values
instead of having to hardcode the numeric variable
"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse

import urlparse
from django.http import QueryDict
from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.auth import REDIRECT_FIELD_NAME


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


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

"""
Decorator to ensure you can only edit your own profile
unless you are an admin or mod
"""
def user_is_self_or_admin( request, viewed_user ):
    if not request.user.is_authenticated():
        messages.error(request, _('You need to be logged in.'))
        return HttpResponseRedirect( settings.LOGIN_URL )

    if request.user != viewed_user and (not request.user.is_staff and not request.user.is_superuser ):
        messages.error(request, _('You are trying to access someones profile without permission. You are a very norty person.'))
        return HttpResponseRedirect( settings.LOGIN_URL )

    return True

