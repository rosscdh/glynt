# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _

from glynt.apps.document.models import DocumentTemplate
from models import FlyForm


class DocumentInline(admin.TabularInline):
  model = DocumentTemplate
  exclude = ['slug', 'summary', 'body', 'doc_status', 'is_public', 'doc_cats']
  readonly_fields = ['name', 'owner' ,'link']
  extra = 0
  can_delete = False
  verbose_name = _('Associated Document')
  verbose_name_plural = _('Associated Document')

  def link(self, obj):
    url = reverse('admin:document_document_change', args=(obj.pk,))
    return mark_safe('<a href="%s">%s</a>' % (url, _('Edit Document'),))
  # the following is necessary if 'link' method is also used in list_display
  link.allow_tags = True

# class FlyFormAdmin(admin.ModelAdmin):
#     inlines = [
#       DocumentInline
#     ]


admin.site.register([FlyForm])
