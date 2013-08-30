# -*- coding: utf-8 -*-

class AjaxBaseTemplateMixin(object):
    """
    Mixin to provide "base_template" context variable
    which will use the ajax base-slim.html template or plain base.html template
    """
    def get_context_data(self, *args, **kwargs):
        context = super(AjaxBaseTemplateMixin, self).get_context_data(*args, **kwargs)

        context.update({
            'base_template': 'base-slim.html' if self.request.is_ajax() else 'base.html',
        })

        return context