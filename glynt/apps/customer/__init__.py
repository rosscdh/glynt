# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class CustomerRequiredViewMixin(object):
    """
    Mixin to ensure that only a lawyer user 
    can view this view
    """
    @method_decorator(user_passes_test(lambda u: u.profile.is_customer))
    def dispatch(self, *args, **kwargs):
        return super(CustomerRequiredViewMixin, self).dispatch(*args, **kwargs)