# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class LawyerRequiredViewMixin(object):
    """
    Mixin to ensure that only a lawyer user 
    can view this view
    """
    @method_decorator(user_passes_test(lambda u: u.profile.is_lawyer))
    def dispatch(self, *args, **kwargs):
        return super(LawyerRequiredViewMixin, self).dispatch(*args, **kwargs)