# -*- coding: utf-8 -*-
from django import template


class TemplateRendererMixin(object):
    """ mixin to allow the testing of template tags and other 
    """
    def render_template(self, *args, **kwargs):
        context = kwargs.get('context', {})
        t = template.Template(''.join(args))
        c = template.Context(context)
        return t.render(c)
