# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext as _

from glynt.apps.document.models import DocumentTemplate


class DocumentTemplatePlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Document Template Plugin")
    render_template = "document/cms_plugins/public-gallery_list.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object_list': DocumentTemplate.public_objects.all(),
            'placeholder': placeholder
        })
        return context

plugin_pool.register_plugin(DocumentTemplatePlugin)